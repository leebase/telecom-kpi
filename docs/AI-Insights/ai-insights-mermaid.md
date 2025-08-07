graph TD
    A[Raw KPI Data from existing app] --> B{Data Adapter}
    B --> C[Standardized KPI Input]

    C --> IE(Insight Engine Module)

    subgraph Insight Engine Core
        IE --> D[KPI Config YAML/JSON]
        IE --> E{Context Builder}
        E --> F[Prompt Templates External]
        F --> G(LLM Abstraction Layer)
        G --> H(LLM Provider - OpenRouter/LiteLLM)
        H --> I{Response Parser}
        I --> J[Insight Post-Processor]
    end

    J --> K[Structured Insights Output]
    K --> L[Dashboard UI Presentation Layer]
    K --> M[Other Consumers e.g., PDF/Email Tool]

    style A fill:#a9d18e,stroke:#38761d,stroke-width:2px
    style L fill:#8eb4d1,stroke:#1d4c76,stroke-width:2px
    style IE fill:#fcd3b4,stroke:#e67e22,stroke-width:2px
