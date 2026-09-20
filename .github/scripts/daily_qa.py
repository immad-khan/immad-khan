#!/usr/bin/env python3
"""
Daily Interview Q&A Generator
Rotates through questions based on the day of the year
"""

import os
from datetime import datetime
import random

# Comprehensive Q&A Database
QUESTIONS = {
    "software_engineering": [
        {
            "q": "What is the difference between a stack and a queue?",
            "a": "Stack: LIFO (Last In First Out) - like a pile of plates. Queue: FIFO (First In First Out) - like a line at a coffee shop."
        },
        {
            "q": "Explain Big O Notation in simple terms",
            "a": "Big O describes how an algorithm's performance scales as input size grows. O(1) = instant, O(n) = linear, O(n²) = slow for large data."
        },
        {
            "q": "What is the difference between SQL and NoSQL databases?",
            "a": "SQL: Structured, tabular data, uses schemas (MySQL, PostgreSQL). NoSQL: Unstructured, flexible schemas, better for scaling (MongoDB, Redis)."
        },
        {
            "q": "What are the SOLID principles?",
            "a": "S: Single Responsibility, O: Open/Closed, L: Liskov Substitution, I: Interface Segregation, D: Dependency Inversion"
        },
        {
            "q": "What is the difference between processes and threads?",
            "a": "Process: Independent program in memory. Thread: Lightweight unit within a process that shares memory with other threads."
        },
        {
            "q": "What is dependency injection and why use it?",
            "a": "A technique where dependencies are passed to a class instead of creating them inside. Makes code more testable and loosely coupled."
        },
        {
            "q": "What is the CAP theorem?",
            "a": "A distributed system can only guarantee 2 of 3: Consistency, Availability, Partition tolerance. You must choose which 2 to prioritize."
        },
        {
            "q": "Explain the ACID properties",
            "a": "Atomicity (all or nothing), Consistency (valid state), Isolation (concurrent transactions don't interfere), Durability (persisted data is safe)."
        },
        {
            "q": "What is the difference between monolith and microservices?",
            "a": "Monolith: Single codebase, easier to start but harder to scale. Microservices: Multiple small services, more complex but scalable independently."
        },
        {
            "q": "What is a design pattern? Name common ones.",
            "a": "Reusable solutions to common problems. Examples: Singleton, Factory, Observer, Strategy, Decorator, MVC."
        },
    ],
    "ai_ml": [
        {
            "q": "What is the difference between AI, ML, and Deep Learning?",
            "a": "AI: Broad concept of machines acting intelligently. ML: Subset where computers learn from data. DL: Subset using neural networks with many layers."
        },
        {
            "q": "What is the difference between supervised and unsupervised learning?",
            "a": "Supervised: Uses labeled data (know the answers). Unsupervised: Finds patterns in unlabeled data (clustering, dimensionality reduction)."
        },
        {
            "q": "What is overfitting and how to prevent it?",
            "a": "When model memorizes training data instead of learning. Prevention: Cross-validation, regularization, more training data, simpler models."
        },
        {
            "q": "What is a neural network activation function?",
            "a": "A mathematical function that determines if a neuron should 'fire'. Common ones: ReLU, Sigmoid, Tanh. Adds non-linearity to the network."
        },
        {
            "q": "What is the difference between loss, accuracy, and metrics?",
            "a": "Loss: How wrong predictions are (lower is better). Accuracy: % correct predictions. Metrics: Domain-specific measures (F1, AUC, etc.)"
        },
        {
            "q": "What is gradient descent?",
            "a": "An optimization algorithm that iteratively adjusts parameters to minimize the loss function by moving in the direction of steepest descent."
        },
        {
            "q": "What is transfer learning?",
            "a": "Using a pre-trained model on a similar problem as a starting point. Saves time and data. Common in computer vision and NLP."
        },
        {
            "q": "What is the difference between CNN and RNN?",
            "a": "CNN: Great for images/spatial data, uses filters. RNN: Great for sequences/time series, has memory of previous inputs."
        },
        {
            "q": "What are transformers and why are they important?",
            "a": "Architecture using self-attention mechanism. Powers GPT, BERT, etc. Can process sequences in parallel and handle long-range dependencies."
        },
        {
            "q": "What is the difference between precision and recall?",
            "a": "Precision: Of predicted positives, how many are correct. Recall: Of actual positives, how many did we find. Trade-off based on use case."
        },
    ],
    "devops": [
        {
            "q": "What is the difference between Docker and Kubernetes?",
            "a": "Docker: Container platform for building/running containers. Kubernetes: Orchestration system for managing multiple containers across machines."
        },
        {
            "q": "What is CI/CD?",
            "a": "CI: Continuously merging code changes with automated testing. CD: Continuously deploying validated changes to production."
        },
        {
            "q": "What is Infrastructure as Code?",
            "a": "Managing infrastructure through code/files instead of manual processes. Tools: Terraform, Ansible, CloudFormation. Version control + reproducibility."
        },
        {
            "q": "What is the difference between horizontal and vertical scaling?",
            "a": "Vertical: Add more power to existing machine (CPU, RAM). Horizontal: Add more machines to the pool. Horizontal is usually more resilient."
        },
        {
            "q": "What is a load balancer?",
            "a": "Distributes traffic across multiple servers. Types: Layer 4 (TCP/UDP) and Layer 7 (HTTP). Improves availability and performance."
        },
        {
            "q": "What is monitoring vs logging?",
            "a": "Monitoring: Real-time metrics and alerts (CPU, memory, requests). Logging: Detailed event records for debugging and auditing."
        },
        {
            "q": "What are the 12-factor app principles?",
            "a": "Best practices for cloud-native apps: codebase, dependencies, config, backing services, build/release/run, stateless processes, port binding, etc."
        },
        {
            "q": "What is the difference between microservices and monolithic architecture?",
            "a": "Monolith: Single deployable unit. Microservices: Small, independent services communicating via APIs. Trade-off: complexity vs simplicity."
        },
        {
            "q": "What is a reverse proxy?",
            "a": "Server that sits in front of backend servers, forwarding client requests. Benefits: SSL termination, caching, load balancing, security."
        },
        {
            "q": "What is GitOps?",
            "a": "Using Git as source of truth for infrastructure and deployments. Changes to Git automatically trigger deployments. Tools: ArgoCD, Flux."
        },
    ],
    "cybersecurity": [
        {
            "q": "What is the difference between encryption, hashing, and encoding?",
            "a": "Encryption: Reversible with key (confidentiality). Hashing: One-way, fixed output (integrity). Encoding: Reversible, no security purpose (data format)."
        },
        {
            "q": "What is the OWASP Top 10?",
            "a": "Top 10 most critical web security risks: Injection, Broken Auth, XSS, IDOR, Security Misconfig, etc. Updated periodically."
        },
        {
            "q": "What is the difference between symmetric and asymmetric encryption?",
            "a": "Symmetric: Same key for encrypt/decrypt (fast, like AES). Asymmetric: Public key encrypts, private key decrypts (slow, like RSA)."
        },
        {
            "q": "What is a SQL injection attack?",
            "a": "Inserting malicious SQL code via user input. Prevention: Parameterized queries, input validation, least privilege database accounts."
        },
        {
            "q": "What is the CIA triad?",
            "a": "Core security principles: Confidentiality (only authorized access), Integrity (data is accurate), Availability (accessible when needed)."
        },
        {
            "q": "What is XSS (Cross-Site Scripting)?",
            "a": "Injecting malicious scripts into web pages. Types: Stored (saved to DB), Reflected (URL params), DOM-based. Prevention: Input sanitization, CSP."
        },
        {
            "q": "What is the difference between authentication and authorization?",
            "a": "Authentication: Verifying WHO you are (login). Authorization: Verifying WHAT you can access (permissions). Both are essential."
        },
        {
            "q": "What is a zero-day vulnerability?",
            "a": "A previously unknown flaw that attackers discover before developers. Called 'zero-day' because developers have had zero days to fix it."
        },
        {
            "q": "What is the principle of least privilege?",
            "a": "Users and systems should only have the minimum permissions needed to do their job. Limits damage from breaches and errors."
        },
        {
            "q": "What is a honeypot in cybersecurity?",
            "a": "A decoy system to attract and detect attackers. Looks vulnerable but is monitored. Helps study attack patterns and alert on threats."
        },
    ],
    "coding": [
        {
            "q": "What is the difference between var, let, and const in JavaScript?",
            "a": "var: Function-scoped, hoisted. let: Block-scoped, not hoisted. const: Block-scoped, not reassignable (but objects can be mutated)."
        },
        {
            "q": "Explain the difference between == and ===",
            "a": "==: Loose equality, type coercion (1 == '1' is true). ===: Strict equality, no coercion (1 === '1' is false). Always prefer ===."
        },
        {
            "q": "What is a closure in programming?",
            "a": "A function that remembers variables from its outer scope even after that scope has closed. Useful for data privacy and factories."
        },
        {
            "q": "What is the difference between array.push() and array.concat()?",
            "a": "push(): Mutates original array, returns new length. concat(): Returns new array, original unchanged. Spread operator [...arr, item] is also immutable."
        },
        {
            "q": "What is the difference between let and const for objects?",
            "a": "Both prevent reassignment to the variable. But const objects can still have their properties modified. Use Object.freeze() for true immutability."
        },
        {
            "q": "What is a Promise in JavaScript?",
            "a": "An object representing eventual completion/failure of async operations. States: pending, fulfilled, rejected. Replaced by async/await now."
        },
        {
            "q": "What is the difference between null and undefined?",
            "a": "undefined: Variable declared but not assigned. null: Intentionally set to empty/no value. typeof null === 'object' is a known JS bug."
        },
        {
            "q": "What are arrow functions and when to avoid them?",
            "a": "Concise syntax, lexical 'this' binding. Avoid: Object methods (need 'this'), constructors, when you need 'arguments' object."
        },
        {
            "q": "What is memoization?",
            "a": "Caching function results based on inputs. Expensive calculations are computed once, subsequent calls return cached result. Trade-off: memory vs speed."
        },
        {
            "q": "What is the difference between forEach, map, filter, and reduce?",
            "a": "forEach: Execute function for each element (no return). map: Transform each element (returns new array). filter: Keep matching elements. reduce: Accumulate to single value."
        },
    ],
    "networking": [
        {
            "q": "What is the difference between TCP and UDP?",
            "a": "TCP: Reliable, connection-oriented, ordered delivery, slower. UDP: Fast, connectionless, no guarantee of delivery. Choose based on needs."
        },
        {
            "q": "What is the OSI model layers (top to bottom)?",
            "a": "7: Application, 6: Presentation, 5: Session, 4: Transport, 3: Network, 2: Data Link, 1: Physical. 'All People Seem To Need Data Processing' 📚"
        },
        {
            "q": "What is the difference between a router and a switch?",
            "a": "Switch: Operates at Layer 2, connects devices in same network (MAC addresses). Router: Operates at Layer 3, connects different networks (IP addresses)."
        },
        {
            "q": "What is DNS and how does it work?",
            "a": "Domain Name System translates domains to IPs. Flow: Browser cache → Resolver → Root → TLD → Authoritative nameserver. Uses UDP port 53."
        },
        {
            "q": "What is the difference between HTTP and HTTPS?",
            "a": "HTTP: Plain text communication. HTTPS: HTTP + TLS encryption. HTTPS uses ports 443, HTTP uses 80. HTTPS also verifies server identity."
        },
        {
            "q": "What is a CIDR block?",
            "a": "Classless Inter-Domain Routing. Format: IP/prefix (e.g., 192.168.1.0/24). The number after / shows how many bits for the network portion."
        },
        {
            "q": "What is the difference between symmetric and asymmetric routing?",
            "a": "Symmetric: Same path both directions. Asymmetric: Different paths can be taken. Asymmetric routing can cause issues with stateful firewalls."
        },
        {
            "q": "What is NAT (Network Address Translation)?",
            "a": "Maps private IPs to public IP(s) for internet access. Types: Static NAT (1:1), Dynamic NAT (many:many pool), PAT (many:1, port-based)."
        },
        {
            "q": "What is a subnet mask and why is it important?",
            "a": "Defines network vs host portion of an IP address. e.g., /24 means first 24 bits are network, last 8 bits are for hosts (254 usable in /24)."
        },
        {
            "q": "What is the difference between load balancer and reverse proxy?",
            "a": "LB: Distributes traffic across servers, can be hardware/software. Reverse Proxy: Receives requests, forwards to backend, often includes LB."
        },
    ],
}


def get_all_questions():
    """Flatten all questions into a single list with category labels"""
    all_q = []
    for category, qs in QUESTIONS.items():
        for q in qs:
            all_q.append({"category": category, **q})
    return all_q


def get_daily_question():
    """Get a deterministic question based on day of year"""
    all_q = get_all_questions()
    # Use day of year for deterministic selection (changes at midnight UTC)
    day_of_year = datetime.utcnow().timetuple().tm_yday
    index = day_of_year % len(all_q)
    return all_q[index]


def format_question(q_data):
    """Format question for README"""
    category_icons = {
        "software_engineering": "⚙️",
        "ai_ml": "🤖",
        "devops": "🚀",
        "cybersecurity": "🔒",
        "coding": "💻",
        "networking": "🌐",
    }
    
    icon = category_icons.get(q_data["category"], "📚")
    
    return f"""<div align="center">

### {icon} Today's Question: {q_data["category"].replace("_", " ").title()}

**{q_data['q']}**

<details>
<summary>💡 Click to reveal answer</summary>

> {q_data['a']}

</details>

*Question #{datetime.utcnow().timetuple().tm_yday} of {len(get_all_questions())}*
</div>"""


def main():
    # Read current README
    readme_path = os.path.join(os.getcwd(), "README.md")
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Get today's question
    question = get_daily_question()
    formatted = format_question(question)
    
    # Replace the section
    import re
    pattern = r"<!-- START_DAILY_QA -->.*<!-- END_DAILY_QA -->"
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, f"<!-- START_DAILY_QA -->\n{formatted}\n<!-- END_DAILY_QA -->", content, flags=re.DOTALL)
    else:
        # Insert before the first header or at end
        content += f"\n<!-- START_DAILY_QA -->\n{formatted}\n<!-- END_DAILY_QA -->\n"
    
    # Write back
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"✅ Updated README with question about: {question['category']}")


if __name__ == "__main__":
    main()
