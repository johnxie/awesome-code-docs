---
layout: default
title: "Chapter 8: Production Operations and Governance"
nav_order: 8
parent: Devika Tutorial
---


# Chapter 8: Production Operations and Governance

Welcome to **Chapter 8: Production Operations and Governance**. In this part of **Devika Tutorial: Open-Source Autonomous AI Software Engineer**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.

This chapter covers team deployment strategies, security hardening, API cost governance, code review requirements for agent-generated code, and the operational runbooks needed to run Devika safely at scale.

## Learning Goals

- design a team deployment architecture for Devika that enforces access control and audit logging
- implement API cost governance controls that prevent runaway spend from autonomous agent tasks
- define code review and merge policies that are appropriate for agent-generated code
- build operational runbooks for incident response, key rotation, and capacity management

## Governance Checklist

- all LLM API keys are stored in a secrets manager, not in config.toml on disk
- agent-generated code requires human review before merging to protected branches
- API spend is tracked per project with per-day and per-task budget caps
- audit logs capture every task submission, agent invocation, and workspace file write

## Source References

- [Devika README](https://github.com/stitionai/devika/blob/main/README.md)
- [Devika Security Policy](https://github.com/stitionai/devika/blob/main/SECURITY.md)
- [Devika Architecture Docs](https://github.com/stitionai/devika/blob/main/docs/architecture.md)
- [Devika Repository](https://github.com/stitionai/devika)

## Summary

You now have a complete production governance framework for Devika covering security, cost controls, code review policies, and operational runbooks for safe team-scale autonomous coding.

Return to: [Tutorial Index](README.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `src/apis/project.py`

The `create_project` function in [`src/apis/project.py`](https://github.com/stitionai/devika/blob/HEAD/src/apis/project.py) handles a key part of this chapter's functionality:

```py
@project_bp.route("/api/create-project", methods=["POST"])
@route_logger(logger)
def create_project():
    data = request.json
    project_name = data.get("project_name")
    manager.create_project(secure_filename(project_name))
    return jsonify({"message": "Project created"})


@project_bp.route("/api/delete-project", methods=["POST"])
@route_logger(logger)
def delete_project():
    data = request.json
    project_name = secure_filename(data.get("project_name"))
    manager.delete_project(project_name)
    AgentState().delete_state(project_name)
    return jsonify({"message": "Project deleted"})


@project_bp.route("/api/download-project", methods=["GET"])
@route_logger(logger)
def download_project():
    project_name = secure_filename(request.args.get("project_name"))
    manager.project_to_zip(project_name)
    project_path = manager.get_zip_path(project_name)
    return send_file(project_path, as_attachment=False)


@project_bp.route("/api/download-project-pdf", methods=["GET"])
@route_logger(logger)
def download_project_pdf():
    project_name = secure_filename(request.args.get("project_name"))
```

This function is important because it defines how Devika Tutorial: Open-Source Autonomous AI Software Engineer implements the patterns covered in this chapter.

### `src/apis/project.py`

The `delete_project` function in [`src/apis/project.py`](https://github.com/stitionai/devika/blob/HEAD/src/apis/project.py) handles a key part of this chapter's functionality:

```py
@project_bp.route("/api/delete-project", methods=["POST"])
@route_logger(logger)
def delete_project():
    data = request.json
    project_name = secure_filename(data.get("project_name"))
    manager.delete_project(project_name)
    AgentState().delete_state(project_name)
    return jsonify({"message": "Project deleted"})


@project_bp.route("/api/download-project", methods=["GET"])
@route_logger(logger)
def download_project():
    project_name = secure_filename(request.args.get("project_name"))
    manager.project_to_zip(project_name)
    project_path = manager.get_zip_path(project_name)
    return send_file(project_path, as_attachment=False)


@project_bp.route("/api/download-project-pdf", methods=["GET"])
@route_logger(logger)
def download_project_pdf():
    project_name = secure_filename(request.args.get("project_name"))
    pdf_dir = Config().get_pdfs_dir()
    pdf_path = os.path.join(pdf_dir, f"{project_name}.pdf")

    response = make_response(send_file(pdf_path))
    response.headers['Content-Type'] = 'project_bplication/pdf'
    return response

```

This function is important because it defines how Devika Tutorial: Open-Source Autonomous AI Software Engineer implements the patterns covered in this chapter.

### `src/apis/project.py`

The `download_project` function in [`src/apis/project.py`](https://github.com/stitionai/devika/blob/HEAD/src/apis/project.py) handles a key part of this chapter's functionality:

```py
@project_bp.route("/api/download-project", methods=["GET"])
@route_logger(logger)
def download_project():
    project_name = secure_filename(request.args.get("project_name"))
    manager.project_to_zip(project_name)
    project_path = manager.get_zip_path(project_name)
    return send_file(project_path, as_attachment=False)


@project_bp.route("/api/download-project-pdf", methods=["GET"])
@route_logger(logger)
def download_project_pdf():
    project_name = secure_filename(request.args.get("project_name"))
    pdf_dir = Config().get_pdfs_dir()
    pdf_path = os.path.join(pdf_dir, f"{project_name}.pdf")

    response = make_response(send_file(pdf_path))
    response.headers['Content-Type'] = 'project_bplication/pdf'
    return response

```

This function is important because it defines how Devika Tutorial: Open-Source Autonomous AI Software Engineer implements the patterns covered in this chapter.

### `src/apis/project.py`

The `download_project_pdf` function in [`src/apis/project.py`](https://github.com/stitionai/devika/blob/HEAD/src/apis/project.py) handles a key part of this chapter's functionality:

```py
@project_bp.route("/api/download-project-pdf", methods=["GET"])
@route_logger(logger)
def download_project_pdf():
    project_name = secure_filename(request.args.get("project_name"))
    pdf_dir = Config().get_pdfs_dir()
    pdf_path = os.path.join(pdf_dir, f"{project_name}.pdf")

    response = make_response(send_file(pdf_path))
    response.headers['Content-Type'] = 'project_bplication/pdf'
    return response

```

This function is important because it defines how Devika Tutorial: Open-Source Autonomous AI Software Engineer implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[create_project]
    B[delete_project]
    C[download_project]
    D[download_project_pdf]
    E[Gemini]
    A --> B
    B --> C
    C --> D
    D --> E
```
