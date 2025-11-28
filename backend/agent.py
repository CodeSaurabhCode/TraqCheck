from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from config import Config
import operator

class AgentState(TypedDict):
    candidate_name: str
    candidate_email: str
    candidate_phone: str
    candidate_company: str
    candidate_designation: str
    request_message: str
    request_type: str 
    messages: Annotated[Sequence[str], operator.add]

class DocumentRequestAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=Config.OPENAI_API_KEY
        )
        self.graph = self._build_graph()
    
    def _build_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("analyze_candidate", self.analyze_candidate)
        workflow.add_node("generate_email_request", self.generate_email_request)
        workflow.add_node("generate_sms_request", self.generate_sms_request)
        
        workflow.set_entry_point("analyze_candidate")

        workflow.add_conditional_edges(
            "analyze_candidate",
            self.route_request_type,
            {
                "email": "generate_email_request",
                "sms": "generate_sms_request"
            }
        )

        workflow.add_edge("generate_email_request", END)
        workflow.add_edge("generate_sms_request", END)
        
        return workflow.compile()
    
    def analyze_candidate(self, state: AgentState) -> AgentState:
        messages = state.get("messages", [])
        messages.append(f"Analyzing candidate: {state['candidate_name']}")

        if state.get("candidate_email"):
            request_type = "email"
        elif state.get("candidate_phone"):
            request_type = "sms"
        else:
            request_type = "email"
        
        state["request_type"] = request_type
        state["messages"] = messages
        return state
    
    def route_request_type(self, state: AgentState) -> str:
        return state["request_type"]
    
    def generate_email_request(self, state: AgentState) -> AgentState:
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI HR assistant. Generate a professional, personalized email requesting PAN and Aadhaar documents from a candidate.

The email should:
1. Be warm and professional
2. Address the candidate by name
3. Mention their company and designation if available
4. Clearly request both PAN and Aadhaar documents
5. Explain why these documents are needed (identity verification for employment records)
6. Provide clear instructions on how to submit (mention they can upload through our portal)
7. Be concise but friendly

Format the email with a proper subject line and body.
"""),
            ("user", """Generate an email for:
Name: {name}
Email: {email}
Company: {company}
Designation: {designation}

Return the response in this format:
SUBJECT: [subject line]

BODY:
[email body]
""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "name": state["candidate_name"] or "Candidate",
            "email": state["candidate_email"] or "",
            "company": state["candidate_company"] or "your organization",
            "designation": state["candidate_designation"] or "the position"
        })
        
        state["request_message"] = response.content
        messages = state.get("messages", [])
        messages.append("Generated personalized email request")
        state["messages"] = messages
        
        return state
    
    def generate_sms_request(self, state: AgentState) -> AgentState:
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an AI HR assistant. Generate a brief, professional SMS message requesting PAN and Aadhaar documents from a candidate.

The SMS should:
1. Be concise (under 160 characters if possible)
2. Address the candidate by name
3. Clearly request PAN and Aadhaar documents
4. Mention they can upload via the portal
5. Be professional but friendly

Keep it short and actionable.
"""),
            ("user", """Generate an SMS for:
Name: {name}
Phone: {phone}

Return only the SMS text, no formatting.
""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "name": state["candidate_name"] or "Candidate",
            "phone": state["candidate_phone"] or ""
        })
        
        state["request_message"] = response.content
        messages = state.get("messages", [])
        messages.append("Generated personalized SMS request")
        state["messages"] = messages
        
        return state
    
    def request_documents(self, candidate_data: dict) -> dict:

        initial_state = {
            "candidate_name": candidate_data.get("name", ""),
            "candidate_email": candidate_data.get("email", ""),
            "candidate_phone": candidate_data.get("phone", ""),
            "candidate_company": candidate_data.get("company", ""),
            "candidate_designation": candidate_data.get("designation", ""),
            "request_message": "",
            "request_type": "",
            "messages": []
        }
        
        result = self.graph.invoke(initial_state)
        
        return {
            "request_message": result["request_message"],
            "request_type": result["request_type"],
            "messages": result["messages"]
        }
