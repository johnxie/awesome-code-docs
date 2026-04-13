---
layout: default
title: "Chapter 7: Diagnostics, Versioning, and Breaking-Change Management"
nav_order: 7
parent: MCP C# SDK Tutorial
---


# Chapter 7: Diagnostics, Versioning, and Breaking-Change Management

Welcome to **Chapter 7: Diagnostics, Versioning, and Breaking-Change Management**. In this part of **MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Preview-stage SDKs need explicit guardrails for change management.

## Learning Goals

- use SDK diagnostics to catch misuse and compatibility risks early
- apply the repository's versioning policy in dependency planning
- separate protocol/schema shifts from SDK API changes
- reduce upgrade regressions with staged rollout patterns

## Risk-Control Strategy

- treat preview package updates as change events requiring regression testing
- track documented diagnostics and wire them into CI quality gates
- evaluate breaking changes against both API consumers and MCP behavior
- keep a compatibility note per service for protocol revision + SDK package versions

## Source References

- [Diagnostics List](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/list-of-diagnostics.md)
- [Versioning Policy](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/versioning.md)
- [Concepts Documentation Index](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/index.md)

## Summary

You now have a change-management model for keeping C# MCP deployments stable while the SDK evolves.

Next: [Chapter 8: Testing, Operations, and Contribution Workflows](08-testing-operations-and-contribution-workflows.md)

## Source Code Walkthrough

### `src/ModelContextProtocol.Core/McpSession.cs`

The `for` class in [`src/ModelContextProtocol.Core/McpSession.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Core/McpSession.cs) handles a key part of this chapter's functionality:

```cs
///   <item>Sending JSON-RPC requests and receiving responses.</item>
///   <item>Sending notifications to the connected session.</item>
///   <item>Registering handlers for receiving notifications.</item>
/// </list>
/// </para>
/// <para>
/// <see cref="McpSession"/> serves as the base class for both <see cref="McpClient"/> and
/// <see cref="McpServer"/>, providing the common functionality needed for MCP protocol
/// communication. Most applications will use these more specific interfaces rather than working with
/// <see cref="McpSession"/> directly.
/// </para>
/// <para>
/// All MCP sessions should be properly disposed after use as they implement <see cref="IAsyncDisposable"/>.
/// </para>
/// </remarks>
public abstract partial class McpSession : IAsyncDisposable
{
    /// <summary>Gets an identifier associated with the current MCP session.</summary>
    /// <remarks>
    /// Typically populated in transports supporting multiple sessions, such as Streamable HTTP or SSE.
    /// Can return <see langword="null"/> if the session hasn't initialized or if the transport doesn't
    /// support multiple sessions (as is the case with STDIO).
    /// </remarks>
    public abstract string? SessionId { get; }

    /// <summary>
    /// Gets the negotiated protocol version for the current MCP session.
    /// </summary>
    /// <remarks>
    /// Returns the protocol version negotiated during session initialization,
    /// or <see langword="null"/> if initialization hasn't yet occurred.
    /// </remarks>
```

This class is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.

### `src/ModelContextProtocol.Core/McpSession.cs`

The `McpSession` class in [`src/ModelContextProtocol.Core/McpSession.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Core/McpSession.cs) handles a key part of this chapter's functionality:

```cs
/// </para>
/// <para>
/// <see cref="McpSession"/> serves as the base class for both <see cref="McpClient"/> and
/// <see cref="McpServer"/>, providing the common functionality needed for MCP protocol
/// communication. Most applications will use these more specific interfaces rather than working with
/// <see cref="McpSession"/> directly.
/// </para>
/// <para>
/// All MCP sessions should be properly disposed after use as they implement <see cref="IAsyncDisposable"/>.
/// </para>
/// </remarks>
public abstract partial class McpSession : IAsyncDisposable
{
    /// <summary>Gets an identifier associated with the current MCP session.</summary>
    /// <remarks>
    /// Typically populated in transports supporting multiple sessions, such as Streamable HTTP or SSE.
    /// Can return <see langword="null"/> if the session hasn't initialized or if the transport doesn't
    /// support multiple sessions (as is the case with STDIO).
    /// </remarks>
    public abstract string? SessionId { get; }

    /// <summary>
    /// Gets the negotiated protocol version for the current MCP session.
    /// </summary>
    /// <remarks>
    /// Returns the protocol version negotiated during session initialization,
    /// or <see langword="null"/> if initialization hasn't yet occurred.
    /// </remarks>
    public abstract string? NegotiatedProtocolVersion { get; }

    /// <summary>
    /// Sends a JSON-RPC request to the connected session and waits for a response.
```

This class is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.

### `src/ModelContextProtocol.Core/McpSession.cs`

The `that` class in [`src/ModelContextProtocol.Core/McpSession.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Core/McpSession.cs) handles a key part of this chapter's functionality:

```cs
    /// <remarks>
    /// This method provides low-level access to send raw JSON-RPC requests. For most use cases,
    /// consider using the strongly-typed methods that provide a more convenient API.
    /// </remarks>
    public abstract Task<JsonRpcResponse> SendRequestAsync(JsonRpcRequest request, CancellationToken cancellationToken = default);

    /// <summary>
    /// Sends a JSON-RPC message to the connected session.
    /// </summary>
    /// <param name="message">
    /// The JSON-RPC message to send. This can be any type that implements JsonRpcMessage, such as
    /// JsonRpcRequest, JsonRpcResponse, JsonRpcNotification, or JsonRpcError.
    /// </param>
    /// <param name="cancellationToken">The <see cref="CancellationToken"/> to monitor for cancellation requests. The default is <see cref="CancellationToken.None"/>.</param>
    /// <returns>A task that represents the asynchronous send operation.</returns>
    /// <exception cref="InvalidOperationException">The transport is not connected.</exception>
    /// <exception cref="ArgumentNullException"><paramref name="message"/> is <see langword="null"/>.</exception>
    /// <remarks>
    /// <para>
    /// This method provides low-level access to send any JSON-RPC message. For specific message types,
    /// consider using the higher-level methods such as <see cref="SendRequestAsync"/> or methods
    /// on this class that provide a simpler API.
    /// </para>
    /// <para>
    /// The method serializes the message and transmits it using the underlying transport mechanism.
    /// </para>
    /// </remarks>
    public abstract Task SendMessageAsync(JsonRpcMessage message, CancellationToken cancellationToken = default);

    /// <summary>Registers a handler to be invoked when a notification for the specified method is received.</summary>
    /// <param name="method">The notification method.</param>
    /// <param name="handler">The handler to be invoked.</param>
```

This class is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.

### `src/ModelContextProtocol.AspNetCore/StreamableHttpSession.cs`

The `StreamableHttpSession` class in [`src/ModelContextProtocol.AspNetCore/StreamableHttpSession.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.AspNetCore/StreamableHttpSession.cs) handles a key part of this chapter's functionality:

```cs
namespace ModelContextProtocol.AspNetCore;

internal sealed class StreamableHttpSession(
    string sessionId,
    StreamableHttpServerTransport transport,
    McpServer server,
    UserIdClaim? userId,
    StatefulSessionManager sessionManager) : IAsyncDisposable
{
    private int _referenceCount;
    private SessionState _state;
    private readonly object _stateLock = new();

    private int _getRequestStarted;
    private readonly CancellationTokenSource _disposeCts = new();

    public string Id => sessionId;
    public StreamableHttpServerTransport Transport => transport;
    public McpServer Server => server;
    private StatefulSessionManager SessionManager => sessionManager;

    public CancellationToken SessionClosed => _disposeCts.Token;
    public bool IsActive => !SessionClosed.IsCancellationRequested && _referenceCount > 0;
    public long LastActivityTicks { get; private set; } = sessionManager.TimeProvider.GetTimestamp();

    public Task ServerRunTask { get; set; } = Task.CompletedTask;

    public async ValueTask<IAsyncDisposable> AcquireReferenceAsync(CancellationToken cancellationToken)
    {
        // The StreamableHttpSession is not stored between requests in stateless mode. Instead, the session is recreated from the MCP-Session-Id.
        // Stateless sessions are 1:1 with HTTP requests and are outlived by the MCP session tracked by the Mcp-Session-Id.
        // Non-stateless sessions are 1:1 with the Mcp-Session-Id and outlive the POST request.
```

This class is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[for]
    B[McpSession]
    C[that]
    D[StreamableHttpSession]
    A --> B
    B --> C
    C --> D
```
