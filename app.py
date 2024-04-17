import streamlit as st
import difflib
from diff_match_patch import diff_match_patch
import json
import openai
import anthropic
from streamlit_ace import st_ace


# Initialize the diff engine
dmp = diff_match_patch()

# API keys and models
ANTHROPIC_API_KEY = st.secrets["ANTHROPIC_API_KEY"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
openai.api_key = OPENAI_API_KEY

Opus = "claude-3-opus-20240229"
Sonnet = "claude-3-sonnet-20240229"
Haiku = "claude-3-haiku-20240307"


st.set_page_config(
    page_title="AI Live Document Editing",
    page_icon=":memo:",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Sample article text
article = """
The 5 Sweetest/Most Cuddly and Smart Dog Breeds for a Loving Family
1. The Sweetest and Most Cuddly Companions: An Overview
In today's fast-paced world, the bond between humans and their canine companions has become a cherished sanctuary. Amidst the hustle and bustle, cuddly and affectionate dog breeds have emerged as a source of emotional support and unwavering companionship, melting our hearts with their gentle dispositions and eagerness to shower us with love and loyalty.

The growing popularity of these breeds as family pets is a testament to their unique charm and ability to foster a profound emotional connection that transcends mere companionship. Their affectionate nature creates a warm and inviting atmosphere within the home, offering a sense of security and comfort for all members of the household.

"Dogs are considered by many to be best friends, companions, and partners. The bond between pooch and human runs deep, and it's a special relationship you share with your dog. If you're the affectionate type, then you like to show your dog how you feel by giving all of your affection to it, hoping that your dog will return the same." [https://www.farmerpetes.com.au/blogs/blog/most-affectionate-dog-breeds]

While their cuddly nature is undoubtedly endearing, it is crucial to recognize the potential challenges that come with owning such perceptive companions. Proper training and socialization are essential to ensure a harmonious relationship between the dog and its human family. Early exposure to various environments and positive reinforcement techniques can help shape these breeds into well-rounded and well-behaved companions.

Alt text

Choosing the right breed for a loving family environment is a decision that should not be taken lightly. Factors such as temperament, energy levels, and compatibility with children must be carefully considered. Each breed possesses unique characteristics that may make them more suitable for certain lifestyles and living situations.

As we delve into the world of the sweetest and most cuddly dog breeds, we will explore the unique traits that make them ideal companions for families seeking a lifetime of love and loyalty. From the gentle giants to the intelligent cuddlers and the hypoallergenic huggables, these breeds offer a diverse range of personalities and characteristics, ensuring that every family can find their perfect match.

Next_Section_to_Do: 2. The Gentle Giants: Large Cuddly Dog Breeds

2. The Gentle Giants: Large Cuddly Dog Breeds
When it comes to cuddly companions, the gentle giants of the canine world offer a unique blend of affection and loyalty. These larger breeds, such as Newfoundlands, Great Pyrenees, and Bernese Mountain Dogs, are renowned for their gentle dispositions and an innate love for cuddling, making them well-suited for families seeking a devoted and protective companion.

"Bernese Mountain Dogs are "cuddle monsters" that "take the cake" when it comes to being affectionate towards their humans. These "strong farm dogs enjoy cuddling by the fire after a day's work" and are known for giving a "Burner bump" to get their owner's attention by "plowing that head into you if you're not giving them enough love."" [https://www.rd.com/list/affectionate-dog-breeds-that-love-to-cuddle/]

While their imposing size may initially seem intimidating, these gentle giants are often described as gentle, patient, and amiable, with a natural inclination to protect and nurture their families. However, it is crucial to address common concerns associated with larger breeds, such as their space requirements and exercise needs.

According to experts, these breeds thrive in environments that provide ample space for them to move around and engage in regular physical activity. [https://www.thesprucepets.com/cuddly-dog-breeds-4769235] Newfoundlands, for instance, may require a spacious backyard or access to open areas where they can stretch their legs and burn off excess energy.

Breed   Exercise Needs  Living Space Requirements
Newfoundland    Moderate exercise, daily walks  Large home with access to a yard
Great Pyrenees  Moderate exercise, daily walks  Large home with access to a yard
Bernese Mountain Dog    Moderate to high exercise, daily walks/hikes    Large home with access to a yard
Proper socialization and training are essential for these breeds, particularly when introducing them to children. Their sheer size can be overwhelming for young children, and it is crucial to teach both the dog and the child how to interact safely and respectfully.

"When a family is affected by trauma, everyone will react in a different way. Also, it is important to remember that despite the above traumatic reactions, many families look back and see that crises have actually helped them to become closer and stronger. However, don't hesitate to seek professional help if you are uncertain or think your family is struggling to recover. Every family is different but, generally speaking, common changes to family life soon after the event include: Parents may fear for each other's safety and the safety of their children away from home." [https://www.cambridge.org/core/journals/behavioral-and-brain-sciences/article/abs/why-are-children-in-the-same-family-so-different-from-one-another/D9C09DCD1CBD443E1D94C0412AC88E79]

Despite the potential challenges, owning a larger cuddly breed can be an incredibly rewarding experience. These gentle giants are known for their protective instincts and ability to serve as loyal family companions, providing a sense of security and comfort for all members of the household.

Alt text

Next_Section_to_Do: 3. Compact Cuddle Buddies: Small Affectionate Dog Breeds for Families

3. Compact Cuddle Buddies: Small Affectionate Dog Breeds for Families
While larger breeds offer their own unique charm, smaller cuddly companions have captured the hearts of many families. Breeds like Cavalier King Charles Spaniels, Pugs, and French Bulldogs are renowned for their affectionate, lap-dog tendencies, making them ideal for those seeking a constant companion by their side.

"The Cavalier King Charles Spaniel "has the most loving eyes ever, and will get along well with everyone, including little ones and other dogs"" [https://www.cosmopolitan.com/lifestyle/g38889364/most-affectionate-dog-breeds/]

These compact cuddle buddies are often described as velcro dogs, forming strong bonds with their human families and thriving on constant companionship. However, it is essential to address the potential challenges that come with owning smaller breeds, such as their higher energy levels and potential for separation anxiety.

While their size may be deceiving, many of these breeds possess boundless energy and a zest for life. Proper exercise and mental stimulation are crucial to prevent destructive behaviors and ensure a well-balanced companion.

Breed   Energy Level    Potential for Separation Anxiety
Cavalier King Charles Spaniel   Moderate    High
Pug Moderate    Moderate
French Bulldog  Moderate to High    Moderate to High
Socialization and training are equally important for these breeds, particularly when introducing them to children. While their small stature may seem less intimidating, it is crucial to teach children how to interact respectfully and gently with these furry friends.

"Toy Poodles "love to be right in your face, cuddling with you at all times and also like to be constantly active and playing, so make sure you're ready for their level of energy"" [https://www.cosmopolitan.com/lifestyle/g38889364/most-affectionate-dog-breeds/]

Despite the potential challenges, owning a smaller cuddly breed can be an incredibly rewarding experience. These breeds are often praised for their portability, lower grooming needs, and suitability for apartment living, making them an excellent choice for families with limited living spaces or specific lifestyle needs.

Alt text

Next_Section_to_Do: 4. Intelligent Cuddlers: Smart Dog Breeds with Affectionate Personalities

4. Intelligent Cuddlers: Smart Dog Breeds with Affectionate Personalities
While affection and cuddliness are undoubtedly endearing traits, some dog breeds offer an additional layer of mental stimulation, making them ideal companions for families seeking both emotional fulfillment and intellectual engagement. Breeds like Poodles, Golden Retrievers, and Labrador Retrievers are renowned for their intelligence, trainability, and affectionate natures, creating a unique blend of cuddly companionship and cognitive prowess.

According to the Coren Scale of canine intelligence, there are measurable differences in the working intelligence of different dog breeds that can be assessed and compared: This scale is widely accepted as the benchmark for assessing the working intelligence of different dog breeds [https://www.pets4homes.co.uk/pet-advice/the-challenges-of-training-highly-intelligent-dogs.html]

While owning a highly intelligent breed can be incredibly rewarding, it is essential to address the potential challenges that come with these perceptive companions. Their need for mental stimulation and consistent training can be demanding, requiring a dedicated and patient approach from their owners.

Breed   Intelligence Level  Training Needs
Poodle  Highly Intelligent  Consistent, engaging training
Golden Retriever    Highly Intelligent  Consistent, positive reinforcement training
Labrador Retriever  Highly Intelligent  Consistent, reward-based training
Proper socialization and training are crucial for these breeds, not only to ensure well-rounded behavior but also to provide the mental stimulation they crave. Engaging in activities such as obedience training, agility courses, and interactive puzzle toys can help keep their minds sharp and their bodies active.

Common training challenges for intelligent dog breeds may include: Strong will and stubbornness, Need for constant mental stimulation and challenges to prevent boredom, These breeds may require consistent, firm training and plenty of exercise to keep them engaged and well-behaved [https://www.pets4homes.co.uk/pet-advice/the-challenges-of-training-highly-intelligent-dogs.html]

Despite the potential challenges, owning an intelligent, cuddly breed can be an incredibly rewarding experience. These breeds are often praised for their versatility, adaptability, and ability to form strong bonds with family members. Their affectionate nature, combined with their cognitive abilities, creates a unique dynamic that can enrich the lives of their owners in countless ways.

Alt text

Next_Section_to_Do: 5. Hypoallergenic Huggables: Cuddly Dog Breeds for Allergy-Friendly Homes

5. Hypoallergenic Huggables: Cuddly Dog Breeds for Allergy-Friendly Homes
For families with allergies or sensitivities, the prospect of owning a cuddly canine companion may seem like a distant dream. However, the world of hypoallergenic dog breeds offers a solution, allowing allergy sufferers to experience the joy of a furry friend without compromising their health. Breeds like Poodles, Maltese, and Bichon Frise are renowned for their low-shedding coats and cuddly temperaments, making them suitable options for allergy-friendly homes.

"Hypoallergenic dog breeds like miniature schnauzers and Maltese have "curly, tightly-woven coats less prone to shedding and dander release" which can be beneficial for people with allergies." [https://www.dailypaws.com/living-with-pets/pet-compatibility/hypoallergenic-dogs]

While no breed is entirely hypoallergenic, these dogs are less likely to trigger allergic reactions due to their predictable, non-shedding coats. However, it is essential to address the potential challenges that come with owning hypoallergenic breeds, such as their grooming needs and potential for separation anxiety.

Regular grooming is crucial for these breeds to maintain their low-shedding coats and prevent matting or skin irritation. Families may need to invest in professional grooming services or learn proper grooming techniques to keep their furry companions looking and feeling their best.

Breed   Grooming Needs  Potential for Separation Anxiety
Poodle  High    Moderate to High
Maltese High    Moderate to High
Bichon Frise    High    Moderate
Socialization and training are equally important for hypoallergenic breeds, particularly when introducing them to children. These breeds thrive on human companionship and may experience separation anxiety if left alone for extended periods.

"There are no 100% hypoallergenic dog breeds, but many breeds are less allergenic for people with dog allergies" [https://www.akc.org/dog-breeds/hypoallergenic-dogs/]

Despite the potential challenges, owning a hypoallergenic, cuddly breed can be an incredibly rewarding experience for families with allergies. These breeds offer the opportunity to enjoy the companionship and affection of a furry friend while minimizing the risk of allergic reactions. Their adaptability to various living situations and their suitability for families with allergies make them a popular choice for those seeking a cuddly companion.

Alt text

Next_Section_to_Do: 6. Cuddly Companions for Active Families: Energetic Dog Breeds with Affectionate Personalities

6. Cuddly Companions for Active Families: Energetic Dog Breeds with Affectionate Personalities
For families with an active lifestyle, finding a canine companion that can keep up with their pace while providing unwavering affection can be a challenge. However, certain dog breeds offer the perfect blend of high energy levels and cuddly personalities, making them ideal companions for those seeking both physical and emotional fulfillment.

Breeds like Australian Shepherds, Border Collies, and Vizslas are renowned for their boundless energy and affectionate natures, creating a unique dynamic that caters to the needs of active families.

According to experts, the level of exercise a dog needs is largely influenced by their breed: Things to consider are energy levels, size, physical limitations, and mental stimulation needs. Dogs generally require anywhere from 30 minutes up to 2 hours of exercise every day depending on their breed. [https://fairmountpetservice.com/Blog/pet-services-blog/dog-walking/dog-exercise-needs-breed-guide-chart/]

While owning a highly energetic breed can be incredibly rewarding, it is essential to address the potential challenges that come with these active companions. Their exercise and mental stimulation needs can be demanding, requiring a dedicated and consistent approach from their owners.

Breed   Energy Level    Exercise Needs
Australian Shepherd High    1-2 hours of vigorous exercise daily
Border Collie   High    1-2 hours of vigorous exercise daily
Vizsla  High    1-2 hours of vigorous exercise daily
Proper socialization and training are crucial for these breeds, not only to ensure well-rounded behavior but also to provide the mental stimulation they crave. Engaging in activities such as agility training, hiking, and other outdoor adventures can help keep their minds sharp and their bodies active.

"Contrary to popular belief, dogs need more than just physical exercise, and brain games can help burn off excess energy." [https://www.puppyleaks.com/more-mental-stimulation/]

Despite the potential challenges, owning an energetic, cuddly breed can be an incredibly rewarding experience for active families. These breeds are often praised for their ability to serve as exercise companions, their adaptability to various living situations, and their potential for forming strong bonds with active family members. Their affectionate nature, combined with their boundless energy, creates a unique dynamic that can enrich the lives of their owners in countless ways.

Alt text

Next_Section_to_Do: 7. Embracing the Cuddly Companion: A Lifetime of Love and Loyalty

7. Embracing the Cuddly Companion: A Lifetime of Love and Loyalty
As we have explored the diverse world of cuddly and affectionate dog breeds, one thing has become abundantly clear: these furry companions have the power to enrich our lives in ways that transcend mere companionship. From the gentle giants to the intelligent cuddlers, and the hypoallergenic huggables, each breed offers a unique blend of characteristics that cater to the specific needs and lifestyles of loving families.

When selecting a cuddly, affectionate dog breed for a loving family environment, it is crucial to consider factors such as temperament, energy levels, and compatibility with children. While some breeds thrive in larger homes with ample outdoor space, others are better suited for apartment living or families with specific lifestyle needs.

"Responsible dog breeders are experts in their breed's health, heritable defects, temperament, and behavior, gained through breeding, historical research, ongoing study, mentoring relationships, club memberships, showing, raising, and training of their select breeds." [https://www.aspca.org/about-us/aspca-policy-and-position-statements/position-statement-criteria-responsible-breeding]

Owning a cuddly canine companion is a lifelong commitment that extends beyond the initial decision to welcome a furry friend into your home. Proper training, socialization, exercise, and veterinary care are essential for ensuring the well-being and happiness of these beloved companions.

"According to Jean Piaget, a Swiss Biologist and Professor of Child Psychology, "intelligence is a form of adaptation, wherein knowledge is constructed by each individual through the two complementary processes of assimilation and accommodation"" [https://www.mondaq.com/turkey/management/526288/adaptation-and-intelligence]

Just as we adapt to the unique needs and personalities of our canine companions, they too adapt to our lifestyles, forming unbreakable bonds that transcend the boundaries of mere pet ownership. It is this mutual adaptation, this willingness to embrace the unique quirks and traits of our furry friends, that truly defines the essence of a loving family environment.

As you embark on the journey of finding your perfect cuddly companion, remember to explore reputable sources and organizations for further information on responsible pet ownership and breed-specific care. The American Kennel Club (AKC) [https://www.akc.org/dog-breeds/] and the ASPCA [https://www.aspca.org/adopt-pet/adoptable-dogs-your-local-shelters] are excellent resources for learning about different breeds and responsible pet ownership practices.

The bond between a family and their canine companion is a sacred one, built on a foundation of love, loyalty, and cherished memories that will last a lifetime. Embrace the journey, cherish the moments, and let the unconditional love of your cuddly companion guide you towards a lifetime of joy and fulfillment.

"""
def compute_diff(old_text, new_text):
    """Compute and format diff between texts using HTML for visibility."""
    diff = dmp.diff_main(old_text, new_text)
    dmp.diff_cleanupSemantic(diff)
    html = dmp.diff_prettyHtml(diff)
    return html.replace('<span>', '<span style="background-color: #D3D3D3;">')  # Apply background color for unchanged parts

def fix_json_with_gpt(json_str, expected_format):
    # Use OpenAI's GPT-3.5-turbo model to fix the JSON string
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert at fixing JSON strings to match the expected format. Do the entire thing without stopping."
            },
            {
                "role": "user",
                "content": f"Fix the following JSON string to match the expected format:\n\nExpected format:\n{expected_format}\n\nJSON string to fix:\n{json_str}"
            }
        ],
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    # Extract the fixed JSON string from the response
    fixed_json = response.choices[0].message.content.strip()
    print(f"Fixed JSON:\n{fixed_json}")
    return fixed_json

def apply_focus_edits(document, focus, model):
    """
    Applies the focus edits to the document.
    Args:
        document (str): The document to apply the focus edits to.
        focus (str): The focus area for the current iteration.
        model (str): The Claude model to use for generating edits.
    Returns:
        str: The edited document after applying the focus edits.
    """


    system_prompt = f"""
    You are an incredibly thorough and anal NYTimes article editor. You do your edits by focusing on ONE specific editing task and ONLY ONE editing task at a time . Your task to focus on right now is:
    {focus}

    You MUST review the entire original document and provide ALL your task relevant suggested edits for every section, all sections, do not leave anything out. 

    The potential edit types are Replacement(most common), Deletion(less common)

    The number of each depends on the task focus and the needs of the article. Sometimes it will require many replacements and nothing else, sometimes many deletions and nothing else, sometimes both, it is up to you to decide the needs. Be incredibly thorough though.

    Here is an example template:
    

    {{

    "fixed_json": [
        ["the original string 1", "replacement string 1"],
        ["the original string 2", "replacement string 2"],
        ["the original string 3", "replacement string 3"],
        ["the original string 4", "replacement string 4"],
        ["the original string 5", "replacement string 5"],
        ["the original string 6", "replacement string 6"],
        ["the original string 7", "replacement string 7"],
        ["the original string 8", "replacement string 8"],
        ["the original string 9", "[DELETE]"],
        ["the original string 10", "[DELETE]"],
        ["the original string 11", "[DELETE]"],
        ["the original string 12", "[DELETE]"],
        ["the original string 13", "[DELETE]"],
        ["the original string 14", "[DELETE]"],
        ["the original string 15", "[DELETE]"],
        ["the original string 16", "[DELETE]"]
    ]

    }}

    The current document is as follows:
    ##############################
    {document}
    ##############################
    Please provide your suggested edits in the requested JSON format.
    """
    result = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY).messages.create(
        model=model,
        system=system_prompt,
        messages=[
            {"role": "user", "content": "Please provide your suggested edits for the ENTIRE document in the requested format."},
        ],
        max_tokens=2000,
        temperature=0.2,
    )
    response_text = result.content[0].text.strip()
    expected_format = """
{
    "fixed_json": [
        ["original string 1", "replacement string 1"],
        ["original string 3", "replacement string 3"],
        ["original string 5", "replacement string 5"],
        ["original string 7", "replacement string 7"],
        ["original string 9", "replacement string 9"],
        ["original string 11", "replacement string 11"],
        ["original string 13", "replacement string 13"],
        ["original string 15", "replacement string 15"],
        ["original string 2", "[DELETE]"],
        ["original string 4", "[DELETE]"],
        ["original string 6", "[DELETE]"],
        ["original string 8", "[DELETE]"],
        ["original string 10", "[DELETE]"],
        ["original string 12", "[DELETE]"],
        ["original string 14", "[DELETE]"],
        ["original string 16", "[DELETE]"]
    ]
}
    """
    fixed_json = fix_json_with_gpt(response_text, expected_format)
    print(f"Fixed Replacements: {fixed_json}")
    try:
        fixed_edits = json.loads(fixed_json)
        edits = fixed_edits.get("fixed_json", [])
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error parsing fixed JSON in focus edits: {e}")
        edits = []
    for edit in edits:
        print(edit)
        if len(edit) == 2:
            original_string, replacement_string = edit
            if original_string == "" and replacement_string:
                diff_html = compute_diff("", replacement_string)
                st.markdown(diff_html, unsafe_allow_html=True)
                document += "\n" + replacement_string

            elif replacement_string == "[DELETE]":
                diff_html = compute_diff(original_string, "")
                st.markdown(diff_html, unsafe_allow_html=True)
                document = document.replace(original_string, "")

            elif original_string and replacement_string:
                diff_html = compute_diff(original_string, replacement_string)
                st.markdown(diff_html, unsafe_allow_html=True)
                document = document.replace(original_string, replacement_string)

            else:
                print(f"Skipping invalid edit: {edit}")
        else:
            print(f"Skipping invalid edit in focus edits: {edit}")
    print(f"Edited document after focus edits:\n{document}")
    return document



def main():
    """Main function for the Streamlit app."""
    st.title("Live Document Editing with Visible Changes")
    # User input for article
    uploaded_file = st.file_uploader("Upload your article (text file)", type=["txt"])
    if uploaded_file is not None:
        original_document = uploaded_file.read().decode("utf-8")
    else:
        original_document = ""
    current_document = original_document  # Initialize current document
    # User input for focus areas
    default_focus_areas = [
        "Remove any lines with Next_Section_to_Do: in them, they are writers notes that must be removed, every single one. There is one before each section in most cases."
        "Remove all equivocation from the original document. Have an opinion and stick to it.", 
        "Remove any overt repetition of the same exact information if any. Reword/rephrase any instance where the word or phrase has already been used frequently", 
        "Make the content more actionable/useful try to provide key takeaways when/where appropriate.",
        "Add some of your own personality to the text with idiosyncratic sentences here and there and variations in sentence length with some mild slang additions (few)", 
        "Remove any text that is not part of the article. For instance the instructions on which section is next, and the Alt text placeholders, these can be deleted.",
        "Fix all citations by replacing the footnotes section with the collated cited sources. Inline links in the context need to become superscript markdown links to the corresponding footnote.",
        "Add Markdown tags for headings and subheadings,", 
        "Add Markdown tags for lists, bullets, tables, blockquotes, bold/italic and more. There may be opportunities to convert long sections of text into lists, bullets, checklets etc. Take these opportunities. Also make sure any existing lists, bullets, tables, etc is in perfect markdown.", 
        "Add Markdown tags for headings, subheadings, lists, bullets, tables, blockquotes, bold/italic and more.", 
        "Polish for visual readability/variety/interest in terms of markdown use", 
        "Check for any missing markdown opportunities left and fix any remaining glaring issues."
    ]
    # Initialize a list to store user-selected focus areas
    focus_areas = []
    # Display input fields for users to add focus areas
    for i, default_focus in enumerate(default_focus_areas, start=1):
        focus_input = st.text_input(f"Enter focus area {i}", value=default_focus)
        focus_areas.append(focus_input)
    # Remove empty strings from focus_areas list
    focus_areas = default_focus_areas
    #focus_areas = [focus for focus in focus_areas if focus]
    # User selection for Claude model
    claude_models = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
    selected_model = st.selectbox("Select Claude model", claude_models, index=1)
    if st.button("Apply Focus Edits"):
        # Display the original article
        edits_placeholder = st.empty()
        for focus in focus_areas:
            st.write(f"### Applying focus: {focus}")
            print(f"Applying focus edits: {focus}")
            with edits_placeholder.container():
                current_document = apply_focus_edits(current_document, focus, selected_model)
                st.markdown("---")
        
        # Display the side-by-side diff
        original_lines = original_document.split('\n')
        edited_lines = current_document.split('\n')
        diff = difflib.HtmlDiff().make_table(original_lines, edited_lines, context=True, numlines=2)
        st.markdown(diff, unsafe_allow_html=True)
        
        # Download button for the final article
        st.download_button(
            label="Download Final Article",
            data=current_document,
            file_name="final_article.md",
            mime="text/markdown"
        )

if __name__ == "__main__":
    main()

