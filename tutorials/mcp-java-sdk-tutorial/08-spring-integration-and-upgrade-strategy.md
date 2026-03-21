---
layout: default
title: "Chapter 8: Spring Integration and Upgrade Strategy"
nav_order: 8
parent: MCP Java SDK Tutorial
---


# Chapter 8: Spring Integration and Upgrade Strategy

Welcome to **Chapter 8: Spring Integration and Upgrade Strategy**. In this part of **MCP Java SDK Tutorial: Building MCP Clients and Servers with Reactor, Servlet, and Spring**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


This chapter connects Java core usage with Spring integration and long-term upgrade planning.

## Learning Goals

- decide when to adopt Spring-specific MCP modules
- prevent drift between core SDK behavior and Spring wrappers
- plan upgrade cadence around release and conformance signals
- keep contribution workflows aligned with maintainers

## Upgrade Playbook

- validate core transport behavior first, then layer Spring modules
- test WebFlux and WebMVC paths independently in CI
- track release changes and conformance notes before upgrading
- contribute fixes with scoped PRs and clear issue context

## Source References

- [Spring WebFlux MCP README](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-spring/mcp-spring-webflux/README.md)
- [Spring WebMVC MCP README](https://github.com/modelcontextprotocol/java-sdk/blob/main/mcp-spring/mcp-spring-webmvc/README.md)
- [Java SDK Releases](https://github.com/modelcontextprotocol/java-sdk/releases)
- [Contributing Guide](https://github.com/modelcontextprotocol/java-sdk/blob/main/CONTRIBUTING.md)

## Summary

You now have a long-term operations model for combining Java core MCP and Spring integrations safely.

Next: Continue with [MCP C# SDK Tutorial](../mcp-csharp-sdk-tutorial/)

## Depth Expansion Playbook

## Source Code Walkthrough

### `mcp-core/src/main/java/io/modelcontextprotocol/json/McpJsonDefaults.java`

The `McpJsonDefaults` class in [`mcp-core/src/main/java/io/modelcontextprotocol/json/McpJsonDefaults.java`](https://github.com/modelcontextprotocol/java-sdk/blob/HEAD/mcp-core/src/main/java/io/modelcontextprotocol/json/McpJsonDefaults.java) handles a key part of this chapter's functionality:

```java
 * The initialization of (singleton) instances of this class is different in non-OSGi
 * environments and OSGi environments. Specifically, in non-OSGi environments the
 * {@code McpJsonDefaults} class will be loaded by whatever classloader is used to call
 * one of the existing static get methods for the first time. For servers, this will
 * usually be in response to the creation of the first {@code McpServer} instance. At that
 * first time, the {@code mcpMapperServiceLoader} and {@code mcpValidatorServiceLoader}
 * will be null, and the {@code McpJsonDefaults} constructor will be called,
 * creating/initializing the {@code mcpMapperServiceLoader} and the
 * {@code mcpValidatorServiceLoader}...which will then be used to call the
 * {@code ServiceLoader.load} method.
 * <p>
 * In OSGi environments, upon bundle activation SCR will create a new (singleton) instance
 * of {@code McpJsonDefaults} (via the constructor), and then inject suppliers via the
 * {@code setMcpJsonMapperSupplier} and {@code setJsonSchemaValidatorSupplier} methods
 * with the SCR-discovered instances of those services. This does depend upon the
 * jars/bundles providing those suppliers to be started/activated. This SCR behavior is
 * dictated by xml files in {@code OSGi-INF} directory of {@code mcp-core} (this
 * project/jar/bundle), and the jsonmapper and jsonschemavalidator provider jars/bundles
 * (e.g. {@code mcp-json-jackson2}, {@code mcp-json-jackson3}, or others).
 */
public class McpJsonDefaults {

	protected static McpServiceLoader<McpJsonMapperSupplier, McpJsonMapper> mcpMapperServiceLoader;

	protected static McpServiceLoader<JsonSchemaValidatorSupplier, JsonSchemaValidator> mcpValidatorServiceLoader;

	public McpJsonDefaults() {
		mcpMapperServiceLoader = new McpServiceLoader<>(McpJsonMapperSupplier.class);
		mcpValidatorServiceLoader = new McpServiceLoader<>(JsonSchemaValidatorSupplier.class);
	}

	void setMcpJsonMapperSupplier(McpJsonMapperSupplier supplier) {
```

This class is important because it defines how MCP Java SDK Tutorial: Building MCP Clients and Servers with Reactor, Servlet, and Spring implements the patterns covered in this chapter.

### `mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java`

The `that` class in [`mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java`](https://github.com/modelcontextprotocol/java-sdk/blob/HEAD/mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java) handles a key part of this chapter's functionality:

```java

/**
 * Assertion utility class that assists in validating arguments.
 *
 * @author Christian Tzolov
 */

/**
 * Utility class providing assertion methods for parameter validation.
 */
public final class Assert {

	/**
	 * Assert that the collection is not {@code null} and not empty.
	 * @param collection the collection to check
	 * @param message the exception message to use if the assertion fails
	 * @throws IllegalArgumentException if the collection is {@code null} or empty
	 */
	public static void notEmpty(@Nullable Collection<?> collection, String message) {
		if (collection == null || collection.isEmpty()) {
			throw new IllegalArgumentException(message);
		}
	}

	/**
	 * Assert that an object is not {@code null}.
	 *
	 * <pre class="code">
	 * Assert.notNull(clazz, "The class must not be null");
	 * </pre>
	 * @param object the object to check
	 * @param message the exception message to use if the assertion fails
```

This class is important because it defines how MCP Java SDK Tutorial: Building MCP Clients and Servers with Reactor, Servlet, and Spring implements the patterns covered in this chapter.

### `mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java`

The `providing` class in [`mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java`](https://github.com/modelcontextprotocol/java-sdk/blob/HEAD/mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java) handles a key part of this chapter's functionality:

```java

/**
 * Utility class providing assertion methods for parameter validation.
 */
public final class Assert {

	/**
	 * Assert that the collection is not {@code null} and not empty.
	 * @param collection the collection to check
	 * @param message the exception message to use if the assertion fails
	 * @throws IllegalArgumentException if the collection is {@code null} or empty
	 */
	public static void notEmpty(@Nullable Collection<?> collection, String message) {
		if (collection == null || collection.isEmpty()) {
			throw new IllegalArgumentException(message);
		}
	}

	/**
	 * Assert that an object is not {@code null}.
	 *
	 * <pre class="code">
	 * Assert.notNull(clazz, "The class must not be null");
	 * </pre>
	 * @param object the object to check
	 * @param message the exception message to use if the assertion fails
	 * @throws IllegalArgumentException if the object is {@code null}
	 */
	public static void notNull(@Nullable Object object, String message) {
		if (object == null) {
			throw new IllegalArgumentException(message);
		}
```

This class is important because it defines how MCP Java SDK Tutorial: Building MCP Clients and Servers with Reactor, Servlet, and Spring implements the patterns covered in this chapter.

### `mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java`

The `Assert` class in [`mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java`](https://github.com/modelcontextprotocol/java-sdk/blob/HEAD/mcp-core/src/main/java/io/modelcontextprotocol/util/Assert.java) handles a key part of this chapter's functionality:

```java

/**
 * Assertion utility class that assists in validating arguments.
 *
 * @author Christian Tzolov
 */

/**
 * Utility class providing assertion methods for parameter validation.
 */
public final class Assert {

	/**
	 * Assert that the collection is not {@code null} and not empty.
	 * @param collection the collection to check
	 * @param message the exception message to use if the assertion fails
	 * @throws IllegalArgumentException if the collection is {@code null} or empty
	 */
	public static void notEmpty(@Nullable Collection<?> collection, String message) {
		if (collection == null || collection.isEmpty()) {
			throw new IllegalArgumentException(message);
		}
	}

	/**
	 * Assert that an object is not {@code null}.
	 *
	 * <pre class="code">
	 * Assert.notNull(clazz, "The class must not be null");
	 * </pre>
	 * @param object the object to check
	 * @param message the exception message to use if the assertion fails
```

This class is important because it defines how MCP Java SDK Tutorial: Building MCP Clients and Servers with Reactor, Servlet, and Spring implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[McpJsonDefaults]
    B[that]
    C[providing]
    D[Assert]
    E[must]
    A --> B
    B --> C
    C --> D
    D --> E
```
