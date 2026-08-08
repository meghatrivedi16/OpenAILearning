# This code defines a Pricing Assistant agent that can perform various pricing-related calculations using multiple tools. 
# The agent can handle complex queries that require 
# chaining multiple tools together, such as applying discounts, calculating taxes, determining profit margins, and estimating shipping costs.

from agents import Agent, Runner, function_tool, set_trace_processors
from dotenv import load_dotenv
from langsmith.wrappers import OpenAIAgentsTracingProcessor

load_dotenv()

@function_tool
async def calculate_discount(price: float, percent: float) -> str:
    """Calculate discounted price.
    
    Args:
        price: Original price.
        percent: Discount percentage from 0 to 100.
    """
    discounted = price * (1 - percent / 100)
    print("Tool executed: calculate_discount")  # Debug statement to confirm tool execution
    return f"Discounted price is ${discounted:.2f}"

@function_tool
async def calculate_tax(price: float, tax_rate: float) -> str:
    """Calculate the final price after applying sales tax.
    
    Args:
        price: The pre-tax price.
        tax_rate: The tax rate percentage (e.g., 8.5 for 8.5%).
    """
    final_price = price * (1 + tax_rate / 100)
    print("Tool executed: calculate_tax")  # Debug statement to confirm tool execution
    return f"Price after {tax_rate}% tax is ${final_price:.2f}"

@function_tool
async def calculate_profit_margin(cost: float, revenue: float) -> str:
    """Calculate the gross profit margin percentage.
    
    Args:
        cost: The cost to produce or acquire the item.
        revenue: The final selling price.
    """
    if revenue <= 0:
        return "Error: Revenue must be greater than 0."
    margin = ((revenue - cost) / revenue) * 100
    print("Tool executed: calculate_profit_margin")  # Debug statement to confirm tool execution
    return f"Gross profit margin is {margin:.2f}%"

@function_tool
async def calculate_shipping_cost(weight_kg: float, distance_km: float, express_shipping: bool = False) -> str:
    """Calculate shipping cost based on weight, distance, and shipping speed.
    
    Args:
        weight_kg: Weight of the package in kilograms.
        distance_km: Delivery distance in kilometers.
        express_shipping: True for express delivery, False for standard.
    """
    base_rate = 5.00
    weight_charge = weight_kg * 1.50
    distance_charge = distance_km * 0.05
    
    total = base_rate + weight_charge + distance_charge
    if express_shipping:
        total *= 1.5  # 50% premium for express
    print("Tool executed: calculate_shipping_cost")  # Debug statement to confirm tool execution
    return f"Shipping cost is ${total:.2f}"

@function_tool
async def calculate_installment(price: float, months: int, interest_rate: float = 0.0) -> str:
    """Calculate monthly installment payments.
    
    Args:
        price: Total price to be financed.
        months: Number of months for the installment plan.
        interest_rate: Annual interest rate percentage (0 for interest-free).
    """
    if months <= 0:
        return "Error: Months must be greater than 0."
        
    if interest_rate == 0:
        monthly = price / months
        return f"Monthly payment (0% APR) is ${monthly:.2f} for {months} months."
        
    # Standard amortization formula
    monthly_rate = (interest_rate / 100) / 12
    monthly_payment = price * (monthly_rate * (1 + monthly_rate)**months) / ((1 + monthly_rate)**months - 1)
    print("Tool executed: calculate_installment")  # Debug statement to confirm tool execution
    return f"Monthly payment ({interest_rate}% APR) is ${monthly_payment:.2f} for {months} months."

# --- Agent Definition ---
set_trace_processors([OpenAIAgentsTracingProcessor()])   # Debugging and tracing processor for the agent

agent = Agent(
    name="Pricing Assistant",
    instructions=(
        "You are a comprehensive Pricing Assistant. Help users calculate prices, taxes, "
        "shipping costs, profit margins, and installment plans. "
        "Chain multiple tools together if a user asks a complex question "
        "(e.g., applying a discount first, then adding tax, then calculating shipping)."
    ),
    tools=[
        calculate_discount, 
        calculate_tax, 
        calculate_profit_margin, 
        calculate_shipping_cost,
        calculate_installment
    ],
)

# --- Execution ---

# A complex query that requires the agent to route between multiple tools
query = (
    "I have a product that costs me $50 to make. I usually sell it for $120. "
    "If I give a 15% discount, add 8% tax, and ship it express (2kg, 150km), "
    "what is the total cost to the customer? Also, what is my profit margin "
    "based on the discounted price (before tax and shipping)?"
)

result = Runner.run_sync(agent, query)
print(result.final_output)