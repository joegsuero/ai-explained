# AI Implementation Series: From Symbolic to Statistical Intelligence

A comprehensive collection of production-ready implementations showcasing the complete spectrum of artificial intelligence paradigms. Each project demonstrates a different AI approach with practical, runnable code and clear explanations.

## Series Overview

This repository serves as a practical companion to the educational blog series _"Beyond Machine Learning: Filling the Gaps in AI"_. It provides hands-on implementations of all major AI paradigms, from classical symbolic systems to modern statistical approaches.

### **What This Series Demonstrates**

Most educational content focuses exclusively on Machine Learning, but artificial intelligence encompasses much more. This series fills that gap by showing:

1. **Symbolic AI is not obsolete** - It powers many critical business systems
2. **Different problems require different approaches** - No single AI paradigm fits all
3. **Explainability matters** - Especially in regulated industries
4. **Hybrid systems are the future** - Combining the best of both worlds

## Architecture Philosophy

Each project follows these principles:

- **Production-ready code**: Not just educational snippets, but architecturally sound implementations
- **Minimal dependencies**: Focus on core concepts without heavyweight frameworks
- **Clear separation of concerns**: Business logic, AI engine, and interface are distinct
- **Full transparency**: Every decision and inference is explainable
- **Progressive complexity**: Starts simple, builds to sophisticated systems

## Project Catalog

### **Part 1: Symbolic & Knowledge-Based AI**

| Project                                                      | Paradigm                 | Description                                            | Key Concepts                                                                   |
| ------------------------------------------------------------ | ------------------------ | ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| **[01-rule-based-ai](01-rule-based-ai/)**   | Rule-Based Systems       | Credit decision engine using explicit business rules   | Forward-chaining inference, transparent decision-making, business rule engines |

## Getting Started

### **Prerequisites**

```bash
# Python 3.9 or higher
python --version

# Git
git --version
```

### **Installation**

```bash
git clone https://github.com/joegsuero/ai-explained.git

# Install dependencies per project (recommended)
cd ai-explained/01-rule-based-ai
pip install -r requirements.txt
```

### **Running Projects**

Each project is self-contained with its own documentation:

```bash
cd ai-explained/01-rule-based-ai

# Read project-specific instructions
cat README.md

python app.py runserver
```

## Educational Value

### **What You'll Learn**

1. **The AI Spectrum**: Understand when to use which type of AI
2. **Implementation Patterns**: Real-world architectural patterns for AI systems
3. **Trade-off Analysis**: Strengths and weaknesses of each approach
4. **Integration Strategies**: How different AI paradigms can work together
5. **Production Considerations**: Beyond proof-of-concept to deployable systems

### **Comparative Insights**

Through these implementations, you'll discover:

- **Rule-based systems** excel where transparency and control are critical
- **Statistical ML** shines with large datasets and pattern recognition
- **Neural networks** dominate perceptual tasks and complex mappings
- **Hybrid approaches** combine the strengths of multiple paradigms
- **Symbolic AI** remains essential for domains requiring explicit reasoning

## Theoretical Foundations

Each implementation is grounded in established AI theory:

- **Symbolic AI**: Based on formal logic, knowledge representation, and automated reasoning
- **Machine Learning**: Rooted in statistics, probability theory, and optimization
- **Neural Networks**: Inspired by computational neuroscience and parallel distributed processing
- **Hybrid Systems**: Combining symbolic and sub-symbolic approaches for complementary strengths

## Project Selection Guide

Use this guide to choose the right implementation for your needs:

| Your Goal                      | Recommended Project              | Why                                   |
| ------------------------------ | -------------------------------- | ------------------------------------- |
| **Need explainable decisions** | 01-rule-based-credit             | Transparent rule-based reasoning      |
| **Have structured knowledge**  | 02-semantic-ecommerce (WIP)            | Explicit knowledge representation     |
<!-- | **Classical data analysis**    | 03-classical-ml-classification   | Interpretable statistical models      |
| **Understand AI fundamentals** | 04-neural-networks-foundations   | Neural networks from first principles |
| **Image/vision tasks**         | 05-deep-learning-computer-vision | State-of-the-art computer vision      |
| **Recommendation systems**     | 06-hybrid-recommendation         | Combining multiple AI approaches      |
| **Text/language processing**   | 07-nlp-transformers              | Modern natural language understanding | -->
