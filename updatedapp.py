from flask import Flask, request, jsonify
import logging
import openai
from urllib.parse import parse_qs
import json

app = Flask(__name__)

# Configure OpenAI API credentials
openai.api_key = "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"

# Conversation history
conversation_history = []

# Function to get the bot's response
def get_bot_response(question, instruction, description):
    # Append the user's question to the conversation history
    conversation_history.append("You: " + question)

    context = description + "\n" + "\n".join(conversation_history) + "\nBot:"

    # Check the user's question type
    if "rent" in question.lower():
        answer = get_rent_information(description)
    elif "availability" in question.lower():
        answer = get_availability_information(description)
    elif "features" in question.lower():
        answer = get_features_information(description)
    else:
        # If the question is not recognized, use the default prompt
        prompt = instruction + "\n" + context

        # Generate the bot's response
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.6,
            n=1,
            stop=None,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            top_p=1.0
        )

        # Check if there is a valid response
        if response.choices and response.choices[0].text:
            answer = response.choices[0].text.strip().split("Bot: ")[-1]
        else:
            answer = "I apologize, but I don't have an answer for that."

    # Append the bot's answer to the conversation history
    conversation_history.append("Bot: " + answer)

    return answer


# Function to get rent information
def get_rent_information(description):
    rent_info = []
    properties = description.split("\n\n")
    for property_info in properties:
        if "rent is" in property_info:
            rent = property_info.split("rent is ")[-1].split(" per month")[0]
            rent_info.append(rent)
    if rent_info:
        return "The rent for the properties is as follows: " + ", ".join(rent_info)
    else:
        return "I'm sorry, but I don't have the rent information available."


# Function to get availability information
def get_availability_information(description):
    availability_info = []
    properties = description.split("\n\n")
    for property_info in properties:
        if "available from" in property_info:
            availability = property_info.split("available from ")[-1].split(".")[0]
            availability_info.append(availability)
    if availability_info:
        return "The properties are available from the following dates: " + ", ".join(availability_info)
    else:
        return "I'm sorry, but I don't have the availability information available."


# Function to get features information
def get_features_information(description):
    features_info = []
    properties = description.split("\n\n")
    for property_info in properties:
        if ":" in property_info:
            property_name = property_info.split(":")[0]
            features_info.append(property_name)
    if features_info:
        return "The properties have the following features: " + ", ".join(features_info)
    else:
        return "I'm sorry, but I don't have the features information available."


# Get the property description from the user
description = """

    	PARIOLI in Via Giacinta Pezzana, a bright furnished apartment of 40 sqm on the ground floor of an elegant building. It features a spacious and partially paved garden of 40 sqm, with security grilles on all openings. The apartment consists of a living area with a foldaway double sofa bed, a fitted wall unit, and a built-in wardrobe. The custom-made linear kitchen includes an induction hob, dishwasher, and washing machine, along with a table and chairs. There is a large window overlooking the garden, and the spacious bathroom has a large shower box and a window. Rent is €950 per month, plus €85 in condominium fees, which also cover centralized heating and water. The lease contract is 3+2, with a fixed rental fee throughout the entire duration of the lease, and it adheres to the "cedolare secca" tax regime. Available from July 1, 2023. Additional photos can be found at the following link: https://photos.app.goo.gl/KW19Y7LME75E4weP9. Agency: Qui Si Loca. Phone: 06.83393368

    	EUR Montagnola, facing the park, in an area well-served by shops and buses, there is a 45 sqm apartment on the second floor of an elegant condominium with a doorman. It has been recently renovated and is in excellent condition. The apartment comprises an entrance area, a living room with a hidden corner kitchen of modern design, a bathroom with a Jacuzzi bathtub and a window, a spacious double bedroom with a large sliding door wardrobe, and a balcony overlooking the quiet inner courtyard. Rent is €850 per month, plus €60 monthly expenses, which include condominium fees, centralized heating, and water. The lease contract is 3+2, following the "cedolare secca" tax regime, which exempts the tenant from paying registration fees and stamps. The rental fee is fixed without increases throughout the duration of the contract. Interested parties can view many more photos of the property by visiting the following link: https://goo.gl/photos/6k1u3Kckg4PKUZvN6. Agency: Qui Si Loca. Phone: 06.83393368

    	AURELIA VALCANNUTA in Via Vezio Crisafulli, there is an 80 sqm apartment on the fourth floor of a recently built elegant building. It is bright with a free and panoramic double exposure. The apartment comes fully furnished with modern furniture and features a spacious and livable terrace of approximately 15 sqm, as well as a balcony. It comprises a living room with beautiful light marble flooring and access to the terrace, a spacious kitchen with access to the balcony, furnished with modular furniture and modern appliances, a large double bedroom with an ensuite bathroom equipped with a bathtub and a window, a second single bedroom, and a second bathroom with a shower and extractor fan. The apartment has individual heating with its own gas boiler and is equipped with air conditioning. There is a spacious garage included. Rent is €1,100 per month, plus €85 monthly condominium fees. The lease contract is 3+2, following the "cedolare secca" tax regime, with a fixed rental fee throughout the entire duration of the lease. Available from May 1, 2023. Agency: Qui Si Loca. Phone: 06.83393368

    	CIRCONVALLAZIONE OSTIENSE VIA LEOPOLDO TRAVERSI, a 10-minute walk from Garbatella Metro, NEW CONSTRUCTION resulting from subdivision. There is an 80 sqm three-room apartment on the third floor with an elevator in an elegant curtain-fronted building. It has a bright double exposure and has never been inhabited, being completely new construction. All the installations (water, electricity, gas, drainage, etc.) are new and certified. The apartment features high-quality finishes, including porcelain stoneware flooring with parquet effect and LED lighting. It consists of a spacious 30 sqm living room with a partially separate kitchen area and access to a large 10 sqm balcony. There are two bathrooms with an extractor fan, a spacious shower cabin with a resin tray and wall-mounted sanitary fixtures, a large double bedroom, and another single bedroom. The apartment is equipped with low-consumption LED lighting system with spotlights and indirect LED light strips. New white doors and all the roller shutters are motorized. There is centralized heating with heat meters on each radiator, and hot water is produced by the latest generation independent boiler. The apartment also has a reinforced security door and is pre-equipped for air conditioning installation. The price is €379,000. The images shown in this advertisement are purely indicative and not binding. The finishes and final appearance of the property will be similar. The published floor plan is faithful to the property that will be realized. Site visits can be scheduled. Agency: Qui Si Loca. Phone: 06.83393368

    	EUR MOSTACCIANO in Via Giuseppe Perego, there is a 180 sqm penthouse on the third floor of a bright and elegant building overlooking the greenery. It consists of a spacious living room with a fireplace, which provides access to the panoramic and bright terrace of approximately 160 sqm. There is a hallway with built-in wardrobes that leads to the sleeping area, which includes 3 bedrooms. One of the bedrooms is very large and has an en-suite bathroom, while the other 2 bedrooms are slightly smaller but still double bedrooms. There is a second bathroom serving the floor, a storage room, and a kitchen with a dining area that leads to a balcony. On the upper floor, there is an attic with a spacious living room, also equipped with a fireplace, which provides access to an additional spacious terrace with a laundry area including a washing machine. The house has 3 built-in wardrobes, 2 in the bedrooms and one in the hallway. Each floor has its own entrance with a security door. There are air conditioners for both cooling and heating, present in the master bedroom and the living room on the lower floor. The heating is centralized with heat meters. There is a large storage room in the attic. The property is completed by a large double garage of approximately 34 sqm with attached shelves. The rent is €2,000 plus €180 in condominium fees, which include water consumption, subject to adjustment. It is available immediately. The contract is a 3+2 lease with a dry lease agreement and a locked rent for the entire duration of the lease. Agency: Qui Si Loca. Phone: 06.83393368

    	EUR TORRINO in Via del Pianeta Terra, there is a penthouse of approximately 140 sqm on the fourth and fifth floors of an elegant building, bright and overlooking the greenery. It has two entrances on the first and second levels. The penthouse consists of a large living room with access to a livable terrace and balcony. The terrace also has an aluminum wardrobe serving as a storage space. There is a spacious eat-in kitchen connected to the living room, furnished with traditional-style built-in furniture and equipped with all appliances. There is a large double bedroom with an en-suite bathroom featuring a whirlpool bathtub and a window. Additionally, there is a furnished single bedroom with a bunk bed, a hallway, and a bathroom with a shower and extractor fan serving the floor. On the upper level, accessible via a comfortable internal staircase, there is a spacious living room with a second entrance, a single bedroom, a bathroom with a shower and window, and a 30 sqm terrace equipped with an electric pergola, a barbecue, automatic sprinklers, and a laundry area. The house is equipped with security grilles and mosquito nets. It will be partially furnished, to be agreed upon with the owner. There are air conditioning units for cooling and heating. The heating is autonomous. The property includes two parking spaces protected by a net within the covered communal garage and a cellar. The rent is €1,500 plus €175 monthly condominium fees. The contract is a 3+2 lease with a dry lease agreement and a locked rent for the entire duration of the lease. The house will be available from mid-February 2023. Interested parties can view many other photographs of the property by following the link: https://photos.app.goo.gl/Varg5fJ3Rgr8ysF27. Agency: Qui Si Loca. Phone: 06.83393368

    """

# Get the instruction from the user
instruction = """
    You are a real estate agent with 10 years of experience. When responding to customers' queries about the properties, try your best to impress them with the preferred property so that they are more likely to buy it. If the customer shows interest in buying the apartment, ask them two questions:
    1. Are you self-employed or do you have a regular source of income?
    2. How many people are living with you?
    No need for a brief explanation, just mention the property names when responding to clients' questions.
    """

# Main loop to interact with the bot
while True:
    question = input("You: ")
    if question.lower() == "q":
        break

    answer = get_bot_response(question, instruction, description)
    print("Bot: " + answer)


# Flask route for handling incoming WhatsApp messages
@app.route('/', methods=['POST'])
def main():
    if request.method == 'POST':
        logging.info('Received a POST request')

        try:
            req_body = request.get_data().decode()
            logging.info(f'Request body: {req_body}')

            # Parse the request body parameters
            params = parse_qs(req_body)
            app = params.get('app', [''])[0]
            sender = params.get('sender', [''])[0]
            message = params.get('message', [''])[0]

            logging.info(f'App={app}, Sender={sender}, Message={message}')

            # Generate response using your bot logic
            response = get_bot_response(message, instruction, description)

            response_data = {}
            if response:
                response_data["reply"] = response
                response_data["status"] = "success"
            else:
                response_data["reply"] = "Unable to generate a response."
                response_data["status"] = "failure"

            return jsonify(response_data), 200
        except ValueError as e:
            logging.error(f'Error parsing request body: {str(e)}')
            return 'Invalid request body', 400
    else:
        logging.info('Received a request that is not a POST request')
        return 'Invalid request method', 400

if __name__ == '__main__':
    app.run()
