import streamlit as st
import pandas as pd
import os
import time
from typing import List, Dict
from sparrow.prompts.manager import PromptManager
from pathlib import Path
from sparrow import OpenAIClient, save_pred_metrics
from copy import deepcopy
import asyncio
from datetime import datetime


def batch_test(pm: PromptManager, df: pd.DataFrame, prompt_messages: list) -> pd.DataFrame:
    """执行批量测试"""

    client = OpenAIClient(
        base_url=st.session_state.model_config["base_url"],
        api_key=st.session_state.model_config["api_key"],
        concurrency_limit=10,
        max_fpx=100,
    )

    progress_bar = st.progress(0)
    status_text = st.empty()

    # 准备prompt
    messages = deepcopy(prompt_messages)

    # 替换模板中的变量
    df['data'] = df['data'].astype(str)
    messages_list = [pm.set_messages_user_content(messages, user_input) for user_input in df['data']]

    async def iter_results():
        nonlocal client
        iter_result_list = []
        idx = 0
        summary = ""
        async for item in client.iter_chat_completions_batch(
                messages_list=messages_list,
                model=st.session_state.model_config['model'],
                temperature=st.session_state.model_config["temperature"],
                top_p=st.session_state.model_config["top_p"],
                max_tokens=st.session_state.model_config["max_tokens"],
                batch_size=20,
                return_summary=True
        ):
            chunk, summary = item
            idx += 1
            iter_result_list.append(chunk)
            progress = idx / len(df)
            progress_bar.progress(progress)
            status_text.text(f"处理第 {idx}/{len(df)} 条数据...")
        return iter_result_list, summary

    result_list, predict_summary = asyncio.run(iter_results())

    # 更新进度
    progress_bar.progress(1.0)
    status_text.text("处理完成!")
    with st.expander("模型请求统计"):
        st.write(predict_summary)
    now_date = datetime.now().strftime("%y-%m-%d")
    df[f'test_response_{now_date}'] = result_list

    return df


def get_test_files() -> List[str]:
    """获取tests目录下的所有测试文件"""
    if not os.path.exists('tests'):
        os.makedirs('tests')
    return [f for f in os.listdir('tests') if f.endswith(('.csv', '.xlsx', '.xls'))]


def render_batch_testing(pm: PromptManager):
    """渲染批量测试页面"""
    st.header("批量测试")

    # 文件上传
    st.write(
        """\
上传测试文件说明：

- 支持 .csv, .xlsx, .xls 文件
- 文件中必须包含 data 列，该列为测试数据
- 测试完成后，模型预测结果会保存为 test_response_YY-MM-DD 列        
"""
    )
    uploaded_file = st.file_uploader(
        "上传测试文件 (支持 .csv, .xlsx, .xls)",
        type=['csv', 'xlsx', 'xls']
    )

    if uploaded_file:
        # 保存上传的文件
        file_path = os.path.join('tests', uploaded_file.name)
        with open(file_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"文件 {uploaded_file.name} 上传成功!")

    # 获取可用的测试文件
    test_files = get_test_files()

    if not test_files:
        st.warning("未找到测试文件，请先上传")
        return

    # 选择测试文件
    selected_file = st.selectbox(
        "选择测试文件",
        test_files
    )

    test_file_path = os.path.join('tests', selected_file)
    # 读取测试文件
    if test_file_path.endswith('.csv'):
        df = pd.read_csv(test_file_path)
    else:
        df = pd.read_excel(test_file_path)
    # 预览数据
    st.write(df.head())

    # 校验数据
    if 'data' not in df.columns:
        st.error("文件格式错误：请确保文件包含 'data' 列")
        return

    # 选择prompt
    prompt_list = pm.list_prompts()
    if not prompt_list:
        st.warning("未找到可用的prompt")
        return

    selected_prompt = st.selectbox(
        "选择要测试的Prompt",
        prompt_list
    )

    # 确保API key已配置
    if not st.session_state.model_config.get('api_key'):
        st.warning("请先在'配置模型参数'页面配置 API Key")
        return

    # 获取prompt模板
    prompt_messages = pm.get_prompt_messages(selected_prompt)
    if not prompt_messages:
        st.error(f"未找到名为 {selected_prompt} 的prompt")
        return

    with st.expander("模型配置与prompt预览", expanded=False):
        st.write(st.session_state.model_config)
        st.write(prompt_messages)

    # 选择测试前n条数据
    n = st.number_input(
        "选择测试前n条数据",
        min_value=1,
        max_value=len(df),
        value=len(df)
    )
    # 执行测试按钮
    if st.button("执行批量测试"):
        with st.spinner("正在执行批量测试..."):
            results_df = batch_test(
                pm,
                df[:n],
                prompt_messages,
            )

            if results_df is not None:
                # 保存结果
                result_path = Path("test_results")
                if not result_path.exists():
                    result_path.mkdir()
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                result_filename = f"test_results_{timestamp}.xlsx"
                results_df.to_excel(result_path / result_filename, index=False)

                # 显示结果预览
                st.subheader("测试结果预览(前50条)")
                st.dataframe(results_df.head(50))

                # 提供下载链接
                with open(result_path / result_filename, 'rb') as f:
                    st.download_button(
                        "下载测试结果",
                        f,
                        file_name=result_filename,
                        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
