---
title: 企业部署指南
description: 企业级 AI 编程工具部署方案——SSO / 私有化 / 混合云
audience: advanced
difficulty: 🔴
status: published
lastUpdated: 2026-08-13
---

# 企业部署指南

> **TL;DR**：企业部署的关键是安全合规——SSO、私有化、数据隔离是三大支柱。

⏱ 预计阅读时间：7 分钟

## 你能在这里学到

- 企业部署的三种模式
- SSO 集成方案
- 私有化部署方案
- 数据安全与合规

## 三种部署模式

### 1. SaaS 模式

直接使用厂商云服务。

**优势**：部署简单、维护成本低。

**劣势**：数据经过第三方、合规风险。

**适用**：对数据安全要求不高的企业。

### 2. 私有化部署

在企业自己的服务器上部署。

**优势**：数据完全可控、合规性好。

**劣势**：部署复杂、维护成本高。

**适用**：对数据安全要求高的企业（金融、医疗、政府）。

### 3. 混合云模式

核心数据私有化，非核心数据用 SaaS。

**优势**：平衡安全与成本。

**劣势**：架构复杂。

**适用**：大部分企业。

## SSO 集成

### 支持的 SSO 方案

| 工具 | SAML | OAuth | LDAP |
|------|------|-------|------|
| Claude Code | ✅ | ✅ | ✅ |
| Cursor | ✅ | ✅ | ❌ |
| Copilot | ✅ | ✅ | ✅ |

### 集成步骤

1. 在 SSO 提供商（Okta / Azure AD）配置应用
2. 在 AI 工具配置 SSO
3. 测试登录流程
4. 推广到全公司

## 私有化部署

### Claude Code 私有化

Claude Code 支持通过 AWS Bedrock / GCP Vertex AI 私有化部署：

```
企业内网 → Bedrock/Vertex → Claude API
```

**优势**：

- 数据不出 VPC
- 合规性好
- 与云厂商集成

### Cursor 私有化

Cursor 支持自定义 API Key，可以连接私有模型：

```
Cursor → 自定义 API → 私有模型
```

### Copilot 私有化

GitHub Enterprise 支持私有化部署：

```
GitHub Enterprise Server → Copilot → 私有模型
```

## 数据安全

### 数据分类

| 类型 | 风险 | 处理方式 |
|------|------|----------|
| 公共代码 | 低 | 可用 SaaS |
| 内部代码 | 中 | 建议私有化 |
| 敏感代码 | 高 | 必须私有化 |
| 密钥/凭证 | 极高 | 禁止上传 |

### 数据隔离

- **项目隔离**：不同项目数据不共享
- **团队隔离**：不同团队数据不共享
- **环境隔离**：开发/测试/生产数据隔离

## 合规要求

### 国内合规

- **数据安全法**：数据分类分级
- **个人信息保护法**：个人信息处理
- **网络安全法**：网络安全保障

### 国际合规

- **GDPR**：欧盟数据保护
- **SOC 2**：安全控制
- **ISO 27001**：信息安全管理

## 常见坑

**1. 不要忽略合规**

不同行业有不同的合规要求。部署前了解清楚。

**2. 不要忽略培训**

员工需要了解数据安全规范。

**3. 不要忽略监控**

监控 AI 工具的使用情况，发现异常及时处理。

## 参考

- [Claude Code 企业部署](/claude-code/ecosystem/enterprise)
- [AWS Bedrock](https://aws.amazon.com/bedrock/)
- [GCP Vertex AI](https://cloud.google.com/vertex-ai)

## 下一步

- 安全合规 → [安全与合规](./security)
- 成本控制 → [成本控制](./cost)

## 如果你想

- 学习 Claude Code → [Claude Code 精通](/claude-code/)
- 团队工作流 → [团队 AI 工作流](../workflows/team)
