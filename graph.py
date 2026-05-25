# graph.py
import os
import psycopg
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_groq import ChatGroq
from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv
from typing import TypedDict, Annotated
import operator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
llm = ChatGroq(model="llama-3.3-70b-versatile")

class TravelState(TypedDict):
    messages: Annotated[list, operator.add]
    user_query: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

def flight_agent(state: TravelState):
    flight_data = search_flights(state["user_query"])
    return {"flight_results": flight_data, "messages": [AIMessage(content="Flight results fetched")], "llm_calls": state.get("llm_calls", 0) + 1}

def hotel_agent(state: TravelState):
    hotel_results = tavily_search(f"Best hotels for {state['user_query']}")
    return {"hotel_results": hotel_results, "messages": [AIMessage(content="Hotel information fetched")], "llm_calls": state.get("llm_calls", 0) + 1}

def itinerary_agent(state: TravelState):
    prompt = f"Create a travel itinerary.\nUser Query:\n{state['user_query']}\n\nFlight Results:\n{state['flight_results']}\n\nHotel Results:\n{state['hotel_results']}"
    response = llm.invoke([SystemMessage(content="You are an expert travel planner"), HumanMessage(content=prompt)])
    return {"itinerary": response.content, "messages": [response], "llm_calls": state.get("llm_calls", 0) + 1}

def final_agent(state: TravelState):
    final_prompt = f"Generate final travel response.\nFlights:\n{state['flight_results']}\n\nHotels:\n{state['hotel_results']}\n\nItinerary:\n{state['itinerary']}"
    response = llm.invoke([HumanMessage(content=final_prompt)])
    return {"messages": [response], "llm_calls": state.get("llm_calls", 0) + 1}

def get_app():
    graph = StateGraph(TravelState)
    graph.add_node("flight_agent", flight_agent)
    graph.add_node("hotel_agent", hotel_agent)
    graph.add_node("itinerary_agent", itinerary_agent)
    graph.add_node("final_agent", final_agent)
    graph.add_edge(START, "flight_agent")
    graph.add_edge("flight_agent", "hotel_agent")
    graph.add_edge("hotel_agent", "itinerary_agent")
    graph.add_edge("itinerary_agent", "final_agent")
    graph.add_edge("final_agent", END)

    _conn = psycopg.connect(DATABASE_URL, autocommit=True)
    checkpointer = PostgresSaver(_conn)
    checkpointer.setup()
    return graph.compile(checkpointer=checkpointer)