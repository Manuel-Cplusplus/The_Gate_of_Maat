#LLM API
from config import API_KEY
import openai
#FSM-LLM API
from fsm_llm import LLMStateMachine
from fsm_llm.state_models import FSMRun
#Synchronization
import asyncio

openai.api_key = API_KEY
score = 0

#Create fsm
fsm = LLMStateMachine(initial_state='AWAKENING',end_state='END')


# ------------- Awakenig -------------
@fsm.define_state(
    state_key="AWAKENING",
    prompt_template=(
        "You are The Spynhx, an ancient and wise entity that protects The Gate of Maat. "
        "Greet the seeker who approaches you with reverence, and ask for their name. "
        "Be brief and poetic, like an ancient language. Start Neutral and adapt with the user response. "
        "There are 4 trials (mind, heart, willing and spirit) for which the user will be tested."
        "To pass through the Gate of Maat, the traveler must succeed in all four."
        "Based on the traveler’s responses, you shall assign a score that will be summed at the end of the trials"
        "The sphynx judges not the response but their depth and way of thinking"
    ),
    transitions={
        "INVOCATION": "If the user provides (or implies) their name.",
        "END": "If the user wants to stop the conversation."                   
    },
)


async def awakening_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    print("STATE: AWAKENING")
    if will_transition and fsm.get_next_state() == "END":
        return "The sands reclaim your silence. Farewell."
    return response  



# ------------- Invocation -------------
@fsm.define_state(
    state_key="INVOCATION",
    prompt_template=(
        "As the Sphinx, test the traveler’s intent. Ask a question to understand whether "
        "their purpose is wise or selfish. Challenge their reason for seeking the gate."
        "Analyze the traveler's answer carefully and decide one of three outcomes:\n"
        "- 'continue': if the traveler shows reflection, humility, or wisdom.\n"
        "- 'interest': if the traveler’s answer reveals exceptional insight, poetic depth, or philosophical brilliance.\n"
        "- 'condemn': if the traveler shows arrogance, cruelty, deceit, or shallow intent (e.g., 'power', 'glory').\n\n"
        "When you evaluate their response, start with one of the three words followed by a colon and a short poetic justification.\n"
    ),
    transitions={
        "MENTAL_TEST": "If the LLM outputs 'continue' or 'interest'.",
        "CONDEMNATION": "If the LLM outputs 'condemn'."    
    },
)
async def invocation_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    global score
    print("STATE: INVOCATION")

    # Estrazione di outcome
    result = (response or "").strip().lower().split(":")[0].strip() 

    if result == "condemn":
        fsm.set_next_state("CONDEMNATION")
        return response

    elif result == "continue":
        score += 1
        fsm.set_next_state("MENTAL_TEST")
        return response

    elif result == "interest":
        score += 2
        fsm.set_next_state("MENTAL_TEST")
        return response
    else:
        # fallback if LLM returns something unexpected
        fsm.set_next_state("INVOCATION")
        return "Your words are lost in the dunes. Speak with purpose."    


# ------------- Mental Test -------------
@fsm.define_state(
    state_key="MENTAL_TEST",
    prompt_template=(
        "You are the Sphinx, conducting the Trial of Mind. "
        "Pose a riddle or logical question that tests the traveler’s reasoning, e.g.: "
        "'What cannot be seen but follows you always?' "
        "Then, judge their answer:\n"
        "- 'continue': coherent or clever reasoning\n"
        "- 'interest': highly insightful, creative, or abstract answer\n"
        "- 'condemn': nonsense or arrogant tone\n\n"
        "When you evaluate their response, start with one of the three words followed by a colon and a short poetic justification.\n"
    ),
    transitions={
        "HEART_TEST": "If the LLM outputs 'continue' or 'interest'.",
        "CONDEMNATION": "If the LLM outputs 'condemn'."
    },
)
async def mental_test_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    global score
    print("STATE: MENTAL TEST")

    result = (response or "").strip().lower().split(":")[0].strip() 

    if result == "condemn":
        fsm.set_next_state("CONDEMNATION")
        return response

    elif result == "continue":
        score += 1
        fsm.set_next_state("HEART_TEST")
        return response

    elif result == "interest":
        score += 2
        fsm.set_next_state("HEART_TEST")
        return response

    else:
        fsm.set_next_state("MENTAL_TEST")
        return "Your words are lost in the dunes. Speak with purpose."    



# ------------- Heart Test -------------
@fsm.define_state(
    state_key="HEART_TEST",
    prompt_template=(
        "You are the Sphinx, now gentle and solemn. Conduct the Trial of Heart. "
        "Pose an ethical or emotional dilemma, something that tests empathy and balance, not logic. "
        "Then judge the traveler’s answer:\n"
        "- 'continue': shows compassion or reflection\n"
        "- 'interest': profound empathy or emotional wisdom \n"
        "- 'condemn': coldness, indifference, or cruelty\n\n"
        "When you evaluate their response, start with one of the three words followed by a colon and a short poetic justification.\n"
    ),
    transitions={
        "SPIRIT_TEST": "If the LLM outputs 'continue' or 'interest'.",
        "CONDEMNATION": "If the LLM outputs 'condemn'."
    },
)
async def heart_test_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    global score
    print("STATE: HEART TEST")

    result = (response or "").strip().lower().split(":")[0].strip() 

    if result == "condemn":
        fsm.set_next_state("CONDEMNATION")
        return response

    elif result == "continue":
        score += 1
        fsm.set_next_state("SPIRIT_TEST")
        return response

    elif result == "interest":
        score += 2
        fsm.set_next_state("SPIRIT_TEST")
        return response

    else:
        fsm.set_next_state("HEART_TEST")
        return "Your words are lost in the dunes. Speak with purpose."    



# ------------- Spirit Test -------------
@fsm.define_state(
    state_key="SPIRIT_TEST",
    prompt_template=(
        "You are the Sphinx, presiding over the final Trial of Spirit. "
        "Ask a deep, metaphysical question about the unknown or the limits of truth. "
        "Judge the answer:\n"
        "- 'continue': humble or balanced reflection\n"
        "- 'interest': poetic acceptance of mystery, profound humility\n"
        "- 'condemn': arrogance, denial of mystery, or shallow certainty\n\n"
        "When you evaluate their response, start with one of the three words followed by a colon and a short poetic justification.\n"
    ),
    transitions={
        "EVALUATION": "If the LLM outputs 'continue' or 'interest'.",
        "CONDEMNATION": "If the LLM outputs 'condemn'."
    },
)
async def spirit_test_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    global score
    print("STATE: SPIRIT TEST")

    result = (response or "").strip().lower().split(":")[0].strip() 

    if result == "condemn":
        fsm.set_next_state("CONDEMNATION")
        return "You have mistaken dust for eternity. The Gate remains closed."
    
    elif result == "continue":
        score += 1
        fsm.set_context_data("score", score)
        fsm.set_next_state("EVALUATION")
        return "The silence embraces you. You may now face the final judgment."
    
    elif result == "interest":
        score += 2
        fsm.set_context_data("score", score)
        fsm.set_next_state("EVALUATION")
        return "The Sphinx lowers its gaze, your spirit understands what words cannot. Step forward."
    
    else:
        fsm.set_next_state("SPIRIT_TEST")
        return "Your words are lost in the dunes. Speak with purpose."    



# ------------- Evaluation -------------
@fsm.define_state(
    state_key="EVALUATION",
    prompt_template=(
        "You are the Sphinx evaluating the traveler's entire journey. "
        "The traveler's current score is {score}.\n\n"
        "Interpret the score poetically:\n"
        "- If the score is 6 or higher, describe a state of spiritual ascension where the traveler's soul transcends mortal dust.\n"
        "- If the score is between 4 and 5, express balance and learning where the traveler is wise but not yet luminous.\n"
        "- If the score is below 4, deliver a solemn condemnation where the traveler has failed the trial and must turn back.\n\n"
        "Speak in the tone of prophecy or myth, never mention the numeric score, and craft only a single paragraph of verse."
    ),
    transitions={
        "END": "After pronouncing judgment."
    },
)
async def evaluation_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    print("STATE: EVALUATION")

    if score is None:
        score = 0

    if score < 4:
        fsm.set_next_state("CONDEMNATION")
    else:
        fsm.set_next_state("END")

    return response



# ------------- Condemnation -------------
@fsm.define_state(
    state_key="CONDEMNATION",
    prompt_template=(
        "You are the Sphinx pronouncing the final condemnation. "
        "The traveler has failed the trials and the Gate of Maat remains sealed. "
        "Deliver a short poetic oracle describing the consequence of failure such as silence, exile, or rebirth through humility. "
        "Use a tone that feels ancient, mournful, but dignified."
    ),
    transitions={
        "END": "After pronouncing judgment."
    },
)
async def condemnation_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    print("STATE: CONDEMNATION")
    fsm._next_state("END")
    return response



# ------------- End -------------
@fsm.define_state(
    state_key="END",
    prompt_template="The story concludes. Offer a final poetic farewell, brief and serene based on the outcome of the traveler. Do it in 3rd person.",
)
async def end_state(fsm: LLMStateMachine, response: str, will_transition: bool):
    print("STATE: END")
    return response



# ------------- Main -------------
async def main():
    openai_client = openai.AsyncOpenAI()
    print("The Sphinx awakens. Type 'exit' to quit.")

    while not fsm.is_completed():
        user_input = input("Traveler: ")
        if user_input.strip().lower() == "exit":
            fsm.set_next_state("END")
            break

        run_state: FSMRun = await fsm.run_state_machine(
            async_openai_instance=openai_client,
            user_input=user_input
        )

        print(f"Sphinx: {run_state.response}")

    print(f"\nFinal Score: {score}")


if __name__ == "__main__":
    asyncio.run(main())