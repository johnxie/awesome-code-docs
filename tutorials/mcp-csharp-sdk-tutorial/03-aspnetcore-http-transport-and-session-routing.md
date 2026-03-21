---
layout: default
title: "Chapter 3: ASP.NET Core HTTP Transport and Session Routing"
nav_order: 3
parent: MCP C# SDK Tutorial
---


# Chapter 3: ASP.NET Core HTTP Transport and Session Routing

Welcome to **Chapter 3: ASP.NET Core HTTP Transport and Session Routing**. In this part of **MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows**, you will build an intuitive mental model first, then move into concrete implementation details and practical production tradeoffs.


HTTP deployment patterns in C# should be explicit about route scoping and per-session behavior.

## Learning Goals

- deploy MCP endpoints with ASP.NET Core integration
- design per-route/per-session tool availability safely
- avoid overexposing tool catalogs across endpoint surfaces
- align HTTP topology with policy and tenant boundaries

## Route and Session Strategy

- expose focused MCP routes for distinct tool domains when possible
- keep all-tools endpoints gated and monitored
- use route-aware filtering for session-specific tool narrowing
- document endpoint semantics so clients can discover expected capability scope

## Source References

- [AspNetCore Package README](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/src/ModelContextProtocol.AspNetCore/README.md)
- [Per-Session Tools Sample](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/samples/AspNetCoreMcpPerSessionTools/README.md)
- [Docs Concepts - HTTP Context](https://github.com/modelcontextprotocol/csharp-sdk/blob/main/docs/concepts/httpcontext/httpcontext.md)

## Summary

You now have an HTTP architecture model for route-scoped MCP services in ASP.NET Core.

Next: [Chapter 4: Tools, Prompts, Resources, and Filter Pipelines](04-tools-prompts-resources-and-filter-pipelines.md)

## Depth Expansion Playbook

## Source Code Walkthrough

### `src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`

The `ParameterInfo` interface in [`src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs) handles a key part of this chapter's functionality:

```cs
        // Extract parameters
        var parameterSyntaxList = methodDeclaration.ParameterList.Parameters;
        ParameterInfo[] parameters = new ParameterInfo[methodSymbol.Parameters.Length];
        for (int i = 0; i < methodSymbol.Parameters.Length; i++)
        {
            var param = methodSymbol.Parameters[i];
            var paramSyntax = i < parameterSyntaxList.Count ? parameterSyntaxList[i] : null;

            parameters[i] = new ParameterInfo(
                ParameterType: param.Type.ToDisplayString(s_fullyQualifiedFormatWithNullability),
                Name: param.Name,
                HasDescriptionAttribute: descriptionAttribute is not null && HasAttribute(param, descriptionAttribute),
                XmlDescription: xmlDocs?.Parameters.TryGetValue(param.Name, out var pd) == true && !string.IsNullOrWhiteSpace(pd) ? pd : null,
                DefaultValue: paramSyntax?.Default?.ToFullString().Trim());
        }

        return new MethodToGenerate(
            NeedsGeneration: true,
            TypeInfo: ExtractTypeInfo(methodSymbol.ContainingType),
            Modifiers: modifiersStr,
            ReturnType: returnType,
            MethodName: methodName,
            Parameters: new EquatableArray<ParameterInfo>(parameters),
            MethodDescription: needsMethodDescription ? xmlDocs?.MethodDescription : null,
            ReturnDescription: needsReturnDescription ? xmlDocs?.Returns : null,
            Diagnostics: diagnostics);
    }

    /// <summary>Checks if XML documentation would generate any Description attributes for a method.</summary>
    private static bool HasGeneratableContent(XmlDocumentation xmlDocs, IMethodSymbol methodSymbol, INamedTypeSymbol descriptionAttribute)
    {
        if (!string.IsNullOrWhiteSpace(xmlDocs.MethodDescription) && !HasAttribute(methodSymbol, descriptionAttribute))
```

This interface is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.

### `src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`

The `TypeInfo` interface in [`src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs) handles a key part of this chapter's functionality:

```cs
        return new MethodToGenerate(
            NeedsGeneration: true,
            TypeInfo: ExtractTypeInfo(methodSymbol.ContainingType),
            Modifiers: modifiersStr,
            ReturnType: returnType,
            MethodName: methodName,
            Parameters: new EquatableArray<ParameterInfo>(parameters),
            MethodDescription: needsMethodDescription ? xmlDocs?.MethodDescription : null,
            ReturnDescription: needsReturnDescription ? xmlDocs?.Returns : null,
            Diagnostics: diagnostics);
    }

    /// <summary>Checks if XML documentation would generate any Description attributes for a method.</summary>
    private static bool HasGeneratableContent(XmlDocumentation xmlDocs, IMethodSymbol methodSymbol, INamedTypeSymbol descriptionAttribute)
    {
        if (!string.IsNullOrWhiteSpace(xmlDocs.MethodDescription) && !HasAttribute(methodSymbol, descriptionAttribute))
        {
            return true;
        }

        if (!string.IsNullOrWhiteSpace(xmlDocs.Returns) &&
            methodSymbol.GetReturnTypeAttributes().All(attr => !SymbolEqualityComparer.Default.Equals(attr.AttributeClass, descriptionAttribute)))
        {
            return true;
        }

        foreach (var param in methodSymbol.Parameters)
        {
            if (!HasAttribute(param, descriptionAttribute) &&
                xmlDocs.Parameters.TryGetValue(param.Name, out var paramDoc) &&
                !string.IsNullOrWhiteSpace(paramDoc))
            {
```

This interface is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.

### `src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`

The `TypeDeclarationInfo` interface in [`src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs) handles a key part of this chapter's functionality:

```cs

        // Build list of nested types from innermost to outermost
        var typesBuilder = ImmutableArray.CreateBuilder<TypeDeclarationInfo>();
        for (var current = typeSymbol; current is not null; current = current.ContainingType)
        {
            var typeDecl = current.DeclaringSyntaxReferences.FirstOrDefault()?.GetSyntax() as TypeDeclarationSyntax;
            string typeKeyword;
            if (typeDecl is RecordDeclarationSyntax rds)
            {
                string classOrStruct = rds.ClassOrStructKeyword.ValueText;
                if (string.IsNullOrEmpty(classOrStruct))
                {
                    classOrStruct = "class";
                }
                typeKeyword = $"{typeDecl.Keyword.ValueText} {classOrStruct}";
            }
            else
            {
                typeKeyword = typeDecl?.Keyword.ValueText ?? "class";
            }

            typesBuilder.Add(new TypeDeclarationInfo(current.Name, typeKeyword));
        }

        // Reverse to get outermost first
        typesBuilder.Reverse();
        
        string ns = typeSymbol.ContainingNamespace.IsGlobalNamespace ? "" : typeSymbol.ContainingNamespace.ToDisplayString();
        return new TypeInfo(ns, new EquatableArray<TypeDeclarationInfo>(typesBuilder.ToImmutable()));
    }

    private static (XmlDocumentation? Docs, bool HasInvalidXml) TryExtractXmlDocumentation(IMethodSymbol methodSymbol)
```

This interface is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.

### `src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`

The `LocationInfo` interface in [`src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs`](https://github.com/modelcontextprotocol/csharp-sdk/blob/HEAD/src/ModelContextProtocol.Analyzers/XmlToDescriptionGenerator.cs) handles a key part of this chapter's functionality:

```cs
    /// causes issues when the generator returns cached data with locations from earlier compilations.
    /// </remarks>
    private readonly record struct LocationInfo(string FilePath, TextSpan TextSpan, LinePositionSpan LineSpan)
    {
        public static LocationInfo? FromLocation(Location? location) =>
            location is null || !location.IsInSource ? null :
            new LocationInfo(location.SourceTree?.FilePath ?? "", location.SourceSpan, location.GetLineSpan().Span);

        public Location ToLocation() =>
            Location.Create(FilePath, TextSpan, LineSpan);
    }

    /// <summary>Holds diagnostic information to be reported.</summary>
    private readonly record struct DiagnosticInfo(string Id, LocationInfo? Location, string MethodName)
    {
        public static DiagnosticInfo Create(string id, Location? location, string methodName) =>
            new(id, LocationInfo.FromLocation(location), methodName);

        public object?[] MessageArgs => [MethodName];
    }

    /// <summary>Holds extracted XML documentation for a method (used only during extraction, not cached).</summary>
    private sealed record XmlDocumentation(string MethodDescription, string Returns, Dictionary<string, string> Parameters);
}

```

This interface is important because it defines how MCP C# SDK Tutorial: Production MCP in .NET with Hosting, ASP.NET Core, and Task Workflows implements the patterns covered in this chapter.


## How These Components Connect

```mermaid
flowchart TD
    A[ParameterInfo]
    B[TypeInfo]
    C[TypeDeclarationInfo]
    D[LocationInfo]
    A --> B
    B --> C
    C --> D
```
