# Product Brief: Slack Equipment Rental Assistant

## Project Overview / Description
A private learning/testing project that demonstrates how a Slack workspace can integrate with external APIs and AI services to provide intelligent equipment recommendations for sound and lighting rental companies. The system operates completely independently, receiving Slack messages from users and responding with AI-powered equipment suggestions based on a simple database of rental equipment.

## Target Audience
- **Primary**: Developers and engineers learning Slack API integration and AI/LLM implementation

## Primary Benefits / Features
- **Seamless Slack Integration**: Users can request equipment recommendations directly through Slack messages (later)
- **Seamless Mock Slack**: Users can request equipment recommendations directly through a mock Slack platform as a flash web app. Mock as a customer requesting details. Easy to migrate to slack later
- **AI-Powered Recommendations**: Cloudflare-based LLM analyzes user requirements and suggests optimal equipment combinations
- **Intelligent Equipment Matching**: Database-driven system with detailed equipment descriptions for accurate AI understanding
- **Package Recommendations**: Equipment grouped into logical categories (e.g., "party package") for easier decision-making
- **Prompt Engineering Flexibility**: Extensive customization options for fine-tuning AI responses and equipment matching logic
- **Simple MCP Integration**: Minimal complexity for equipment understanding and database queries
- **Independent Operation**: Self-contained system that doesn't require external dependencies beyond Slack and Cloudflare

## High-Level Tech/Architecture
- **Frontend**: Slack workspace integration using Slack API
- **Backend**: Independent application server handling message processing
- **AI Engine**: Cloudflare-based LLM for intelligent equipment recommendation
- **Database**: Simple, lightweight database storing equipment details and categories
- **MCP (Model Context Protocol)**: Minimal implementation for equipment understanding
- **API Layer**: RESTful endpoints for equipment queries and AI processing
- **Message Flow**: Slack → API → Database Query → LLM Processing → Response Generation → Slack Reply

## Key Components
1. **Equipment Database**: Structured data with detailed descriptions for AI comprehension
2. **Category System**: Logical grouping of equipment into packages (e.g., "party package", "corporate package")
3. **Prompt Engineering Framework**: Flexible system for customizing AI behavior and responses
4. **Slack Bot**: Handles incoming messages and outgoing responses
5. **Recommendation Engine**: AI-powered logic for matching user needs with available equipment

## Success Metrics
- Accurate equipment recommendations based on user requirements
- Seamless Slack integration with minimal latency
- Flexible prompt engineering capabilities for fine-tuning
- Independent operation without external service dependencies
