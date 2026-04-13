---
layout: default
title: "Chapter 7: Strict Mode, Batching, Logging, and Debugging"
nav_order: 7
parent: MCP Swift SDK Tutorial
---


# Chapter 7: Strict Mode, Batching, Logging, and Debugging

Welcome to **Chapter 7: Strict Mode, Batching, Logging, and Debugging**. In this part of **MCP Swift SDK Tutorial: Building MCP Clients and Servers in Swift**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


Advanced client controls improve reliability when used intentionally.

## Learning Goals

- use strict vs default configuration modes based on risk posture
- apply request batching for throughput-sensitive paths
- instrument logging/debug flows for faster issue isolation
- avoid hiding capability mismatches behind permissive defaults

## Practical Guidance

- enable strict mode for environments with strong protocol guarantees
- keep batching isolated to idempotent or safe request clusters
- log capability negotiation and transport errors with correlation context
- validate non-strict fallback behavior explicitly in tests

## Source References

- [Swift SDK README - Strict vs Non-Strict Configuration](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#strict-vs-non-strict-configuration)
- [Swift SDK README - Request Batching](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#request-batching)
- [Swift SDK README - Debugging and Logging](https://github.com/modelcontextprotocol/swift-sdk/blob/main/README.md#debugging-and-logging)

## Summary

You now have a control model for balancing safety and performance in Swift MCP clients.

Next: [Chapter 8: Release, Versioning, and Production Guidelines](08-release-versioning-and-production-guidelines.md)

## Source Code Walkthrough

### `Sources/MCP/Server/Prompts.swift`

The `CodingKeys` interface in [`Sources/MCP/Server/Prompts.swift`](https://github.com/modelcontextprotocol/swift-sdk/blob/HEAD/Sources/MCP/Server/Prompts.swift) handles a key part of this chapter's functionality:

```swift
    }

    private enum CodingKeys: String, CodingKey {
        case name, title, description, arguments, icons, _meta
    }

    public func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(name, forKey: .name)
        try container.encodeIfPresent(title, forKey: .title)
        try container.encodeIfPresent(description, forKey: .description)
        try container.encodeIfPresent(arguments, forKey: .arguments)
        try container.encodeIfPresent(icons, forKey: .icons)
        try container.encodeIfPresent(_meta, forKey: ._meta)
    }

    public init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        name = try container.decode(String.self, forKey: .name)
        title = try container.decodeIfPresent(String.self, forKey: .title)
        description = try container.decodeIfPresent(String.self, forKey: .description)
        arguments = try container.decodeIfPresent([Argument].self, forKey: .arguments)
        icons = try container.decodeIfPresent([Icon].self, forKey: .icons)
        _meta = try container.decodeIfPresent(Metadata.self, forKey: ._meta)
    }

    /// An argument for a prompt
    public struct Argument: Hashable, Codable, Sendable {
        /// The argument name
        public let name: String
        /// A human-readable argument title
        public let title: String?
```

This interface is important because it defines how MCP Swift SDK Tutorial: Building MCP Clients and Servers in Swift implements the patterns covered in this chapter.

### `Sources/MCP/Base/Value.swift`

The `Foundation` interface in [`Sources/MCP/Base/Value.swift`](https://github.com/modelcontextprotocol/swift-sdk/blob/HEAD/Sources/MCP/Base/Value.swift) handles a key part of this chapter's functionality:

```swift
import struct Foundation.Data
import class Foundation.JSONDecoder
import class Foundation.JSONEncoder

/// A codable value.
public enum Value: Hashable, Sendable {
    case null
    case bool(Bool)
    case int(Int)
    case double(Double)
    case string(String)
    case data(mimeType: String? = nil, Data)
    case array([Value])
    case object([String: Value])

    /// Create a `Value` from a `Codable` value.
    /// - Parameter value: The codable value
    /// - Returns: A value
    public init<T: Codable>(_ value: T) throws {
        if let valueAsValue = value as? Value {
            self = valueAsValue
        } else {
            let data = try JSONEncoder().encode(value)
            self = try JSONDecoder().decode(Value.self, from: data)
        }
    }

    /// Returns whether the value is `null`.
    public var isNull: Bool {
        return self == .null
```

This interface is important because it defines how MCP Swift SDK Tutorial: Building MCP Clients and Servers in Swift implements the patterns covered in this chapter.

### `Sources/MCP/Base/Value.swift`

The `StringInterpolation` interface in [`Sources/MCP/Base/Value.swift`](https://github.com/modelcontextprotocol/swift-sdk/blob/HEAD/Sources/MCP/Base/Value.swift) handles a key part of this chapter's functionality:

```swift
}

// MARK: - ExpressibleByStringInterpolation

extension Value: ExpressibleByStringInterpolation {
    public struct StringInterpolation: StringInterpolationProtocol {
        var stringValue: String

        public init(literalCapacity: Int, interpolationCount: Int) {
            self.stringValue = ""
            self.stringValue.reserveCapacity(literalCapacity + interpolationCount)
        }

        public mutating func appendLiteral(_ literal: String) {
            self.stringValue.append(literal)
        }

        public mutating func appendInterpolation<T: CustomStringConvertible>(_ value: T) {
            self.stringValue.append(value.description)
        }
    }

    public init(stringInterpolation: StringInterpolation) {
        self = .string(stringInterpolation.stringValue)
    }
}

// MARK: - Standard Library Type Extensions

extension Bool {
    /// Creates a boolean value from a `Value` instance.
    ///
```

This interface is important because it defines how MCP Swift SDK Tutorial: Building MCP Clients and Servers in Swift implements the patterns covered in this chapter.

### `Sources/MCP/Base/Value.swift`

The `Value` interface in [`Sources/MCP/Base/Value.swift`](https://github.com/modelcontextprotocol/swift-sdk/blob/HEAD/Sources/MCP/Base/Value.swift) handles a key part of this chapter's functionality:

```swift

/// A codable value.
public enum Value: Hashable, Sendable {
    case null
    case bool(Bool)
    case int(Int)
    case double(Double)
    case string(String)
    case data(mimeType: String? = nil, Data)
    case array([Value])
    case object([String: Value])

    /// Create a `Value` from a `Codable` value.
    /// - Parameter value: The codable value
    /// - Returns: A value
    public init<T: Codable>(_ value: T) throws {
        if let valueAsValue = value as? Value {
            self = valueAsValue
        } else {
            let data = try JSONEncoder().encode(value)
            self = try JSONDecoder().decode(Value.self, from: data)
        }
    }

    /// Returns whether the value is `null`.
    public var isNull: Bool {
        return self == .null
    }

    /// Returns the `Bool` value if the value is a `bool`,
    /// otherwise returns `nil`.
    public var boolValue: Bool? {
```

This interface is important because it defines how MCP Swift SDK Tutorial: Building MCP Clients and Servers in Swift implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[CodingKeys]
    B[Foundation]
    C[StringInterpolation]
    D[Value]
    E[UnitInterval]
    A --> B
    B --> C
    C --> D
    D --> E
```
