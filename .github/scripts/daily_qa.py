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
         {
    "q": "What are your thoughts on declarative vs. imperative paradigms such as functional and object-oriented programming?",
    "a": "Imperative code describes how to do something step by step (loops, mutable state, OOP methods changing object state). Declarative code describes what result you want (SQL, React JSX, functional pipelines like map/filter/reduce). Declarative/functional code is easier to reason about, test, and parallelize because it avoids side effects. OOP is strong for modeling domain entities and encapsulating state. In practice I mix them: OOP for structure and boundaries, functional style for data transformation, and I pick whichever keeps the code simplest for the problem."
  },
  {
    "q": "What are your most used design patterns and in what contexts do you use them?",
    "a": "Factory (creating objects without hard-coding concrete classes, e.g. payment or notification providers), Singleton (shared resources like config or a DB connection pool, used sparingly), Observer (event systems, UI state updates, pub/sub), Strategy (swappable algorithms like pricing or sorting rules), Repository (separating data access from business logic), and Dependency Injection (testability and loose coupling). I use patterns to solve a real problem, not to add abstraction upfront."
  },
  {
    "q": "What is \"Agile\" software development and what are your thoughts on it?",
    "a": "Agile is an iterative approach where teams deliver small working increments in short sprints, gather feedback continuously, and adapt to changing requirements. I like it because it reduces risk, surfaces problems early, and keeps the team aligned with users. Its weaknesses show when teams skip planning, treat ceremonies as bureaucracy, or let scope creep. It works best with clear priorities, a good backlog, and honest retrospectives."
  },
  {
    "q": "What are your thoughts on software testing?",
    "a": "Testing is essential for confidence when changing code. I follow the test pyramid: many fast unit tests, fewer integration tests, and a small number of end-to-end tests. Tests should be reliable, readable, and focused on behavior rather than implementation. Good tests enable safe refactoring and CI/CD, but 100% coverage is not the goal; meaningful coverage of critical paths and edge cases is."
  },
  {
    "q": "Describe a difficult bug you were tasked with fixing in a large application. How did you debug the issue?",
    "a": "Use the STAR format. Example: an intermittent production error appeared only under load. I reproduced it by checking logs and recent deployments, narrowed it down with breakpoints and added logging, and found a race condition on shared state. I fixed it with proper synchronization/idempotent handling, added a regression test, and documented the root cause. Key points: systematic reproduction, isolating variables, finding root cause rather than patching symptoms, and preventing recurrence."
  },
  {
    "q": "How do you explain technical challenges to stakeholders who do not have technical knowledge or backgrounds?",
    "a": "Avoid jargon, use analogies, and focus on impact: cost, time, risk, and user experience. Lead with the conclusion, then offer options with trade-offs and a recommendation. Use visuals or simple diagrams where helpful, and check understanding by asking for their questions."
  },
  {
    "q": "What aspect of our company, product or team interests you most?",
    "a": "Research the company beforehand and tailor the answer. Structure: (1) a specific product, technology, or mission point you genuinely find interesting, (2) how it connects to your skills and experience, (3) what you hope to learn or contribute. Avoid generic answers like 'good culture' without specifics."
  },
  {
    "q": "How do you determine a project's success?",
    "a": "Success is measured against goals defined upfront: delivered on time and within budget, meets requirements and quality standards, achieves business or user outcomes (adoption, satisfaction, performance metrics, revenue or cost savings), and is maintainable. Post-launch metrics, stakeholder feedback, and team retrospectives confirm whether it truly succeeded."
  },
  {
    "q": "What are the differences between statically and dynamically typed languages?",
    "a": "Statically typed languages (Java, C++, TypeScript) check types at compile time, catching errors early and enabling better tooling and performance. Dynamically typed languages (Python, JavaScript) check types at runtime, offering flexibility and faster prototyping but with more runtime errors."
  },
  {
    "q": "What is the difference between a list and a tuple in Python, and when would you use each?",
    "a": "Lists are mutable, ordered collections ([1, 2, 3]) used when data changes. Tuples are immutable, ordered collections ((1, 2, 3)) used for fixed data such as coordinates or dictionary keys. Tuples are slightly faster and memory-efficient, and are hashable if their contents are hashable."
  },
  {
    "q": "Explain Python's GIL (Global Interpreter Lock) and its implications.",
    "a": "The GIL is a mutex in CPython that allows only one thread to execute Python bytecode at a time, protecting memory management (reference counting). Implication: multithreading does not speed up CPU-bound tasks, but it works well for I/O-bound tasks. For CPU-bound work use multiprocessing, native extensions (NumPy), or alternative implementations."
  },
  {
    "q": "What are Python decorators, and can you write a simple example?",
    "a": "A decorator is a function that wraps another function to add behavior without modifying its code.\n\ndef log(func):\n    def wrapper(*args, **kwargs):\n        print(f'Calling {func.__name__}')\n        return func(*args, **kwargs)\n    return wrapper\n\n@log\ndef greet(name):\n    return f'Hello {name}'"
  },
  {
    "q": "What is a generator in Python, and how does it differ from a list?",
    "a": "A generator produces values lazily one at a time using yield, so it does not store all values in memory. A list stores all elements at once. Generators are memory-efficient for large or infinite sequences but can be iterated only once and do not support indexing."
  },
  {
    "q": "What are *args and **kwargs, and when would you use them?",
    "a": "*args collects extra positional arguments into a tuple; **kwargs collects extra keyword arguments into a dict. Use them for flexible function signatures, decorators, wrappers, and passing arguments through to other functions."
  },
  {
    "q": "What is the difference between var, let, and const?",
    "a": "var is function-scoped, hoisted (initialized as undefined), and can be redeclared. let and const are block-scoped and live in the temporal dead zone until declared. let allows reassignment; const does not (though object contents can still be mutated). Prefer const by default, let when reassigning, and avoid var."
  },
  {
    "q": "Explain the event loop, call stack, and microtask queue in JavaScript.",
    "a": "JavaScript is single-threaded. The call stack runs synchronous code. Async callbacks (timers, I/O) wait in the task (macrotask) queue, while promise callbacks (.then, async/await) go to the microtask queue. When the stack is empty, the event loop runs all microtasks first, then takes the next macrotask. This is why Promise callbacks run before setTimeout(fn, 0)."
  },
  {
    "q": "What is closure in JavaScript, and why is it useful?",
    "a": "A closure is a function that remembers variables from its outer scope even after the outer function has returned. It is useful for data privacy, function factories, callbacks, and maintaining state (e.g. counters, memoization, module pattern)."
  },
  {
    "q": "What is the difference between == and === in JavaScript?",
    "a": "== performs type coercion before comparing; === is strict equality, checking value and type without coercion. Modern style guides mandate === because == produces non-obvious results (e.g., null == undefined is true, but null === undefined is false)."
  },
  {
    "q": "What is prototypal inheritance in JavaScript?",
    "a": "JavaScript doesn't actually use traditional class-based inheritance. Instead, every object has an internal [[Prototype]] link to another object, and property lookups follow this chain. The ES6 class syntax just makes this pattern easier to use."
  },
  {
    "q": "What is the difference between == and .equals() in Java?",
    "a": "== on objects checks reference equality; .equals() checks value equality as defined by the class. For strings, == can return false for identical content that lives in different objects, while .equals() correctly returns true.\n\nString a = new String(\"hello\");\nString b = new String(\"hello\");\nSystem.out.println(a == b);       // false\nSystem.out.println(a.equals(b));  // true"
  },
  {
    "q": "What is the difference between HashMap and ConcurrentHashMap?",
    "a": "HashMap is not thread-safe, so if multiple threads change it at the same time, its data can get corrupted. ConcurrentHashMap is designed for safe use by many threads, using segment-level locking in older Java versions or lock-free methods in Java 8 and later. This makes it much faster than a synchronized HashMap when there's a lot of concurrent access."
  },
  {
    "q": "Explain the difference between an abstract class and an interface in Java.",
    "a": "An abstract class can include both abstract and regular methods, instance fields, and constructors, but a class can only extend one abstract class. An interface (since Java 8) can have default and static methods as well as abstract ones, and a class can implement multiple interfaces. Use an abstract class when you want to share state or behavior, and use interfaces when you want different classes to follow the same contract."
  },
  {
    "q": "What is the difference between checked and unchecked exceptions in Java?",
    "a": "Checked exceptions (subclasses of Exception, not RuntimeException) must be caught or declared via throws; they represent recoverable conditions (IOException, SQLException). Unchecked exceptions (subclasses of RuntimeException) need no declaration and usually signal programming errors (NullPointerException, ArrayIndexOutOfBoundsException)."
  },
  {
    "q": "How does Java's garbage collection work, and what are the main GC algorithms?",
    "a": "The JVM splits the heap into different areas: young (for new objects), old or tenured (for long-lived objects), and metaspace (for class metadata). Minor garbage collection cleans the young generation often, while major or full garbage collection cleans the whole heap less frequently. Common algorithms: Serial GC (single-threaded, small heaps), Parallel GC (throughput), G1 GC (default since JDK 9, balanced), and ZGC or Shenandoah (very large heaps with very short pause times)."
  },
  {
    "q": "What is the Stream API in Java, and when should you use it?",
    "a": "Introduced in Java 8, the Stream API processes collections in a declarative, functional style, supporting lazy evaluation and parallelization via .parallelStream(). Use it when transforming, filtering, or aggregating data in a readable, pipeline-oriented way.\n\nList<String> result = names.stream()\n    .filter(n -> n.startsWith(\"A\"))\n    .map(String::toUpperCase)\n    .sorted()\n    .collect(Collectors.toList());"
  },
  {
    "q": "How would you design a URL shortener like bit.ly?",
    "a": "Clarify requirements first: read/write ratio (likely ~100:1 reads), scale, URL expiry, analytics. Core components: a web service for redirect/shorten requests, a hashing function for short codes (Base62 encoding of a counter, or a truncated hash), a key-value store for URL mappings (DynamoDB, Redis), and a cache layer for the hot read path. Trade-offs: a distributed counter avoids collisions but needs coordination; random generation with retries is simpler but has a small collision risk. Cache the most popular ~20% of URLs and put a CDN or edge cache in front of the redirect service."
  },
  {
    "q": "How would you design a rate limiter?",
    "a": "Common algorithms: Token Bucket (tokens refill at a fixed rate, allowing bursts), Leaky Bucket (requests flow out at a fixed rate, excess queued/dropped), Fixed Window Counter (simple, but vulnerable to boundary spikes), and Sliding Window Log (precise, but memory-intensive). For distributed systems, store counters in Redis with TTL-based expiry, using Lua scripts or atomic operations to avoid race conditions across instances. Decide explicitly whether to fail open or fail closed when the limiter itself is unavailable."
  },
  {
    "q": "How would you design a notification system that sends emails, push notifications, and SMS?",
    "a": "Separate what to send from how to send it. An event producer publishes to a message queue (Kafka/SQS); a notification service consumes events, checks user preferences, renders templates, and routes to the right vendor (SendGrid, APNs/FCM, Twilio). Use a dead-letter queue for failed deliveries, and store history for auditing and deduplication. Key concerns: idempotency, per-user rate limiting, and graceful degradation when a vendor API is down."
  },
  {
    "q": "What is the CAP theorem, and how does it affect database selection?",
    "a": "A distributed system can guarantee at most two of three properties: Consistency, Availability, and Partition Tolerance. Since network partitions are unavoidable, the real choice is between CP (consistent but may be unavailable during a partition) and AP (available but may serve stale data). HBase and Zookeeper favor CP; DynamoDB and Cassandra favor AP."
  },
  {
    "q": "Walk me through designing a real-time chat application.",
    "a": "Clients connect to a WebSocket server for persistent, real-time communication. A message service handles durable storage, while a presence service tracks online status. For offline users, a notification service pushes messages through alternate channels. For cross-server messaging, a broker such as Kafka sits between the WebSocket servers and the storage layer, so a message sent by User A on Server 1 reaches User B on Server 2. For storage, use an append-heavy, time-series-friendly database like Cassandra, with messages indexed by conversation ID and timestamp for efficient pagination."
  },
  {
    "q": "What is the difference between monolithic and microservices architecture?",
    "a": "A monolith is built as one large, tightly connected unit. It's easier to develop and launch at first but harder to scale and maintain as it grows. Microservices split the application into smaller, loosely connected services that communicate through APIs. Each service can be scaled and maintained independently, but deployment and monitoring become more complex."
  },
  {
    "q": "How do you handle scaling a web application?",
    "a": "Vertical scaling adds more resources (CPU, RAM) to a single server. Horizontal scaling spreads the workload across several servers by adding more machines. Horizontal scaling is usually preferred because it is more reliable and handles failures better, especially with load balancers. As applications grow, it is often combined with caching (Redis) and database sharding to boost performance and scalability."
  },
  {
    "q": "What is the difference between an array and a linked list?",
    "a": "An array is contiguous memory with O(1) index access, though resizing is expensive. A linked list is a chain of nodes with O(1) insertion/deletion (given the node) but O(n) access, since nodes must be traversed sequentially. Prefer linked lists for frequent insertions/deletions; arrays for fast indexed access."
  },
  {
    "q": "Explain the concept of a binary search tree (BST).",
    "a": "Each node has at most two children; the left subtree contains smaller values, and the right subtree contains larger ones. This enables searching, insertion, and deletion in typically O(log n) time (O(n) if the tree becomes unbalanced), making BSTs common for dynamic datasets needing frequent updates and lookups."
  },
  {
    "q": "What is Agile methodology, and why is it popular?",
    "a": "Agile focuses on working in short cycles, teamwork, and flexibility. Teams deliver small updates in short sprints. It is popular because it adapts easily to changing requirements, provides quick feedback, and allows frequent releases of working software."
  },
  {
    "q": "What is the difference between Agile and Waterfall methodologies?",
    "a": "Agile is iterative: requirements can change and feedback is added throughout each sprint. Waterfall is sequential: each phase is finished before the next starts, and requirements are set early. Agile works best for projects that may change; Waterfall is better for projects with clear, fixed requirements."
  },
  {
    "q": "What is normalization in databases, and why is it important?",
    "a": "Normalization organizes a relational database into related tables to reduce redundancy and improve data integrity, eliminating duplicate data and preventing anomalies like inconsistent updates or deletion errors."
  },
  {
    "q": "What is the difference between SQL and NoSQL databases?",
    "a": "SQL databases are relational and use structured schemas and SQL queries (MySQL, PostgreSQL), making them great for organized, structured data. NoSQL databases are non-relational and store data as key-value pairs, documents, or graphs (MongoDB, Cassandra). They handle large amounts of unstructured or semi-structured data better, but often trade some strict data guarantees for flexibility."
  },
  {
    "q": "What is unit testing, and why is it important?",
    "a": "Unit testing checks each part or function of your code in isolation, helping you find bugs early and providing ongoing documentation of expected behavior. Test-driven development (TDD), where you write tests before the code, is a common way to apply it."
  },
  {
    "q": "What is continuous integration (CI)?",
    "a": "CI means regularly merging code into a shared repository, where each update is automatically built and tested. This avoids integration issues, keeps the code ready to deploy, and speeds up releases using tools like Jenkins or GitLab CI."
  },
  {
    "q": "How do you approach debugging a production issue under time pressure?",
    "a": "Start by collecting logs and error messages to understand the problem. Try to reproduce the issue in a staging environment, or if that's not possible, check recent deployments and changes. Focus on quick fixes like rolling back or restarting while you work on a long-term solution, and keep your team and stakeholders updated throughout."
  },
  {
    "q": "Describe a time you improved the performance of an application.",
    "a": "A strong answer names the specific bottleneck (e.g., redundant database joins), the fix (indexing, lazy loading, caching), and a measurable result (e.g., a concrete percentage improvement in load time)."
  },
  {
    "q": "What is the difference between multithreading and multiprocessing?",
    "a": "Multithreading runs several threads in the same process; they share memory and communicate quickly, but may hit race conditions. Multiprocessing runs separate processes with their own memory, which is safer but makes communication slower. Multiprocessing is better for CPU-heavy tasks; multithreading works well for tasks that spend time waiting on I/O."
  },
  {
    "q": "What is the purpose of a design pattern in software development?",
    "a": "Design patterns are tried-and-true solutions to common design problems. They make code easier to maintain, scale, and reuse, and give teams a common language to discuss solutions. Examples: Singleton, Factory, Observer."
  },
  {
    "q": "How do you ensure the maintainability of your code?",
    "a": "Make each function do one thing, use clear and meaningful names, and write unit tests to catch issues when you make changes later. Treat code reviews and refactoring as regular parts of your workflow, not occasional tasks."
  },
  {
    "q": "What is version control, and why is it important in software development?",
    "a": "Version control tracks and manages changes to your code over time. It makes collaboration easier, allows branching for new features, and lets you roll back if something goes wrong. Git is the most widely used system today."
  },
  {
    "q": "What is SQL injection, and how can you prevent it?",
    "a": "SQL injection inserts malicious SQL through input fields to manipulate the database, such as bypassing authentication or extracting/deleting data. Prevent it with parameterized queries or prepared statements, input validation and sanitization, ORM frameworks, and minimal database permissions."
  },
  {
    "q": "How would you deploy an application in the cloud?",
    "a": "Choose a cloud provider like AWS, Azure, or GCP. Set up a virtual machine or use a container platform like Kubernetes, depending on your needs. Use Infrastructure as Code tools like Terraform or CloudFormation to make the setup repeatable. Automate deployments with CI/CD pipelines, and use scaling rules and monitoring to keep the app running smoothly as traffic changes."
  },
  {
    "q": "How do you use AI coding assistants like GitHub Copilot in your development workflow?",
    "a": "Use AI assistants to boost productivity, but don't rely on them to make decisions for you. They're most helpful for repetitive code, test setup, and explaining unfamiliar code. Always review suggestions for accuracy, security, and fit with your project. They are less reliable for complex business logic or security-sensitive code."
  },
  {
    "q": "How do you review AI-generated code for quality and security?",
    "a": "Review it like any other code: check edge cases, security issues like injection, leaked secrets or logs, error handling, coding style, and test coverage. Be especially careful with authentication, authorization, and cryptography code, since AI models can suggest insecure patterns. Do a second security review for these cases."
  },
  {
    "q": "What is the difference between a large language model (LLM) and a traditional rule-based system, and when would you choose each?",
    "a": "Rule-based systems use clear, set rules, so behavior is predictable and easy to verify. LLMs learn from large amounts of data and handle messy, natural-language input, but their answers aren't always predictable or reliable. Use rule-based systems when results must be easily verifiable (e.g. a discount calculator). Use LLMs for unstructured text or when writing out all the rules is impractical."
  },
  {
    "q": "How would you build a simple AI-powered feature, and what concerns would you raise before shipping it?",
    "a": "Pick a model API, design the prompt or fine-tune the model, create a set of test cases, and set limits for speed and cost. Before launch, consider the risk of wrong answers, response latency, per-use cost at scale, data privacy (whether user data goes to a third party), monitoring, and a fallback if the model is unavailable."
  },
  {
    "q": "What is prompt injection, and how would you defend against it in a product that uses LLMs?",
    "a": "Prompt injection is when someone uses crafted input to change how a language model behaves, making it follow new or harmful instructions. Defend by keeping system instructions separate from user input, using structured roles instead of string concatenation, validating and cleaning inputs, limiting what the model can do with sensitive operations, treating its output as untrusted until verified, and monitoring for unusual results."
  },
  {
    "q": "Have you worked with any machine learning pipelines? What were the main engineering challenges?",
    "a": "Common challenges: ensuring clean, high-quality data; differences between training and production environments; tracking model versions and keeping results reproducible; monitoring for drift in real-world data; and managing latency and cost at scale. Tools like MLflow, Kubeflow, and Feast help, but don't solve all of these completely."
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
