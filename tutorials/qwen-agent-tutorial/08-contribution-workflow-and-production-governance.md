---
layout: default
title: "Chapter 8: Contribution Workflow and Production Governance"
nav_order: 8
parent: Qwen-Agent Tutorial
---


# Chapter 8: Contribution Workflow and Production Governance

Welcome to **Chapter 8: Contribution Workflow and Production Governance**. In this part of **Qwen-Agent Tutorial: Tool-Enabled Agent Framework with MCP, RAG, and Multi-Modal Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter closes with contribution strategy and team governance patterns.

## Learning Goals

- contribute examples and framework improvements responsibly
- maintain docs/tests along with behavior changes
- enforce secure defaults in deployment playbooks
- preserve observability and auditability in production setups

## Governance Checklist

- review tool and MCP scopes before rollout
- pin model/config versions per environment
- maintain run logs and evaluation evidence
- include security review for sandboxed execution components

## Source References

- [Qwen-Agent Repository](https://github.com/QwenLM/Qwen-Agent)
- [Qwen-Agent Issues](https://github.com/QwenLM/Qwen-Agent/issues)
- [Qwen-Agent Documentation](https://qwenlm.github.io/Qwen-Agent/en/)
- [Qwen Chat](https://chat.qwen.ai/)

## Summary

You now have a complete Qwen-Agent path from first setup to production governance.

Next tutorial: [Mini-SWE-Agent Tutorial](../mini-swe-agent-tutorial/)

## Depth Expansion Playbook

## Source Code Walkthrough

### `examples/multi_agent_router.py`

The `init_agent_service` function in [`examples/multi_agent_router.py`](https://github.com/QwenLM/Qwen-Agent/blob/HEAD/examples/multi_agent_router.py) handles a key part of this chapter's functionality:

```py


def init_agent_service():
    # settings
    llm_cfg = {'model': 'qwen-max'}
    llm_cfg_vl = {'model': 'qwen-vl-max'}
    tools = ['image_gen', 'code_interpreter']

    # Define a vl agent
    bot_vl = Assistant(llm=llm_cfg_vl, name='多模态助手', description='可以理解图像内容。')

    # Define a tool agent
    bot_tool = ReActChat(
        llm=llm_cfg,
        name='工具助手',
        description='可以使用画图工具和运行代码来解决问题',
        function_list=tools,
    )

    # Define a router (simultaneously serving as a text agent)
    bot = Router(
        llm=llm_cfg,
        agents=[bot_vl, bot_tool],
    )
    return bot


def test(
        query: str = 'hello',
        image: str = 'https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg',
        file: Optional[str] = os.path.join(ROOT_RESOURCE, 'poem.pdf'),
):
```

This function is important because it defines how Qwen-Agent Tutorial: Tool-Enabled Agent Framework with MCP, RAG, and Multi-Modal Workflows implements the patterns covered in this chapter.

### `examples/multi_agent_router.py`

The `test` function in [`examples/multi_agent_router.py`](https://github.com/QwenLM/Qwen-Agent/blob/HEAD/examples/multi_agent_router.py) handles a key part of this chapter's functionality:

```py


def test(
        query: str = 'hello',
        image: str = 'https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg',
        file: Optional[str] = os.path.join(ROOT_RESOURCE, 'poem.pdf'),
):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []

    if not image and not file:
        messages.append({'role': 'user', 'content': query})
    else:
        messages.append({'role': 'user', 'content': [{'text': query}]})
        if image:
            messages[-1]['content'].append({'image': image})
        if file:
            messages[-1]['content'].append({'file': file})

    for response in bot.run(messages):
        print('bot response:', response)


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
```

This function is important because it defines how Qwen-Agent Tutorial: Tool-Enabled Agent Framework with MCP, RAG, and Multi-Modal Workflows implements the patterns covered in this chapter.

### `examples/multi_agent_router.py`

The `app_tui` function in [`examples/multi_agent_router.py`](https://github.com/QwenLM/Qwen-Agent/blob/HEAD/examples/multi_agent_router.py) handles a key part of this chapter's functionality:

```py


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        query = input('user question: ')
        # Image example: https://dashscope.oss-cn-beijing.aliyuncs.com/images/dog_and_girl.jpeg
        image = input('image url (press enter if no image): ')
        # File example: resource/poem.pdf
        file = input('file url (press enter if no file): ').strip()
        if not query:
            print('user question cannot be empty！')
            continue
        if not image and not file:
            messages.append({'role': 'user', 'content': query})
        else:
            messages.append({'role': 'user', 'content': [{'text': query}]})
            if image:
                messages[-1]['content'].append({'image': image})
            if file:
                messages[-1]['content'].append({'file': file})

        response = []
        for response in bot.run(messages):
            print('bot response:', response)
        messages.extend(response)


```

This function is important because it defines how Qwen-Agent Tutorial: Tool-Enabled Agent Framework with MCP, RAG, and Multi-Modal Workflows implements the patterns covered in this chapter.

### `examples/multi_agent_router.py`

The `app_gui` function in [`examples/multi_agent_router.py`](https://github.com/QwenLM/Qwen-Agent/blob/HEAD/examples/multi_agent_router.py) handles a key part of this chapter's functionality:

```py


def app_gui():
    bot = init_agent_service()
    chatbot_config = {
        'verbose': True,
    }
    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
    # test()
    # app_tui()
    app_gui()

```

This function is important because it defines how Qwen-Agent Tutorial: Tool-Enabled Agent Framework with MCP, RAG, and Multi-Modal Workflows implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[init_agent_service]
    B[test]
    C[app_tui]
    D[app_gui]
    E[init_agent_service]
    A --> B
    B --> C
    C --> D
    D --> E
```
