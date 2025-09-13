import asyncio
from connection import config 
from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered
from pydantic import BaseModel
import rich 


class PassengerOutput(BaseModel):
    res: str
    isWeightEsceed : bool


airport_security_agent = Agent(
    name = "Airport Security Agent",
    instructions = """Your task is to check passengers luggage,
    if passengers luggage is above 30KGs, Stop them Politely.""",
    output_type = PassengerOutput                       #by default it is always string.
)

# We need to Import Rich. Rich is an external python library that is used to make the terminal output look good. To do that we need to add it in console by add uv add rich.

@input_guardrail
async def security_guardrail(ctx, agent, input):

    result = await Runner.run(
        airport_security_agent,
        input,
        run_config = config
    )
    rich.print(result.final_output)

    return GuardrailFunctionOutput(
        output_info =result.final_output,
        tripwire_triggered = False  
    )

passenger = Agent(
    name = "Passengers",
    instructions = "you are a passenger agent.",
    input_guardrails = [security_guardrail]        # To let the passenger agent know the airport rules, we add input guardrail
)

async def main():
    try:
        result = await Runner.run(passenger, "I have 25KGs of luggage.", run_config = config)
        print(result.final_output)

    except InputGuardrailTripwireTriggered:
        print("Passenger can board the flight.")
   



if __name__ == "__main__":
    asyncio.run(main())