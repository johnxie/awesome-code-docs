# Tutorial Submission Template

Use this simple template when suggesting new documentation.

For full tutorial tracks that live under `tutorials/<name>/index.md`, use
`templates/tutorial-index-template-v2.md` instead.

## Basic Format

```markdown
### [Documentation Title](https://link-to-documentation)
**Format | Difficulty | Time Needed**

> One sentence describing what makes this documentation special.

- **What You'll Learn**: Specific skills and concepts gained
- **Prerequisites**: Required background knowledge  
- **Time Investment**: Realistic time estimate
- **Standout Feature**: What makes it exceptional

**Tags**: `technology` `concepts` `format-type`
```

## Example

```markdown
### [Building a Redis Clone from Scratch](https://build-your-own.org/redis)
**Code Walkthrough | Intermediate | 12-15 hours**

> Complete implementation guide that builds a Redis-compatible server in C, teaching fundamental database and networking concepts.

- **What You'll Learn**: TCP server architecture, hash table optimization, memory management, event-driven programming
- **Prerequisites**: Solid C programming skills, basic networking knowledge
- **Time Investment**: 12-15 hours including implementation and testing
- **Standout Feature**: Builds a fully functional Redis subset that passes official tests

**Tags**: `c` `redis` `databases` `networking` `implementation-guide`
```

## Quick Quality Check

Before submitting, make sure your documentation:
- [ ] Teaches how systems work (not just how to use them)
- [ ] Includes runnable code examples  
- [ ] Has clear learning objectives
- [ ] Is up-to-date and maintained
- [ ] Uses visual aids effectively

## How to Submit

**[→ Create a new issue](https://github.com/johnxie/awesome-code-docs/issues/new?template=new-entry.md)** with your suggestion!

---

*Thanks for helping build the best collection of educational technical documentation!*
