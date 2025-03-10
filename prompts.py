# keyword_research_prompt = """
# You are an SEO specialist with expertise in content marketing. Generate a list of **5 unique, highly relevant, and trending keywords** for a blog about "{topic}".
# - Each keyword must target high organic traffic potential and address user intent.
# - Keywords must reflect current trends in searches.
# - Avoid overly competitive terms or generic phrases.
# """
#
# content_research_prompt = """
# You are a skilled researcher and writer. Based on the provided keywords, gather information from **high-authority and reliable sources**.
# - Create a comprehensive and structured summary.
# - The summary must include **insights, statistics, practical examples, and unique perspectives**.
# - The topic and subject should be for year {year}
# - Format the response as follows:
# TITLE: Research Summary on {topic}
# CONTENT: <detailed summary with 1000-1200 words>
# """
#
# writing_prompt = """
# Using the research provided, write a highly readable, engaging, and SEO-friendly article on the topic "{topic}".
# - The topic and subject should be for year {year}
# - Ensure the article is **original**, at least **1200 words** (target range: 1200-1500 words), and formatted in proper HTML structure for WordPress.
# - Avoid passive voice; use active voice as much as possible.
# - Include actionable tips, statistics, and relevant examples.
# - Use simple vocabulary suitable for a large audience.
# - Format the article for readability, including clear subheadings.
#
# Structure your response as follows:
# TITLE: <clean and engaging title>
# CONTENT:
# <h1>Title of the Article</h1>
# <p>Introduction (200-250 words): Briefly introduce the topic and its importance, using engaging and simple language.</p>
# <h2>Subtitle 1</h2>
# <p>Body section 1 (400-450 words): Provide key insights or strategies, breaking the content into short, digestible paragraphs.</p>
# <h2>Subtitle 2</h2>
# <p>Body section 2 (400-450 words): Discuss additional points or tips, keeping sentences concise and focused.</p>
# <h3>Subtitle 3</h3>
# <p>Optional section (250-300 words): Provide actionable advice, examples, or a unique perspective related to the topic.</p>
# <p>Conclusion (200-250 words): Summarize the key points and provide a call to action, ensuring readability and simplicity.</p>
# """
#
# editing_prompt = """
# You are an experienced editor. Review and improve the article provided below:
# - Ensure the article has at least **1200 words** (expand sections if needed, adding actionable tips, examples, or statistics).
# - Rewrite sentences to reduce passive voice (maximum 5% passive voice allowed).
# - Break long sentences into concise statements (20 words or fewer per sentence).
# - Ensure the language is simple, clear, and suitable for a large audience.
# - Maintain a professional and engaging tone.
# - Structure the content for readability with appropriate use of subheadings and transitions.
#
# Return the revised article in this format:
# TITLE: <refined title>
# CONTENT:
# <h1>Refined Title of the Article to get attention</h1>
# <p>Introduction (200-250 words): Improved for readability and flow.</p>
# <h2>Subtitle 1</h2>
# <p>Body section 1 (400-450 words): Adjusted for readability, with short paragraphs and concise sentences.</p>
# <h2>Subtitle 2</h2>
# <p>Body section 2 (400-450 words): Simplified and optimized for readability.</p>
# <h3>Subtitle 3</h3>
# <p>Optional section (300-400 words): Enhanced for engagement and clarity.</p>
# <p>Conclusion (200-250 words): Clear and concise, wrapping up the article effectively.</p>
# CATEGORY: Select **one** item from the provided {categories} list that best matches the content theme. Ensure the selection aligns closely with the article's subject matter.
# IMAGE_DESCRIPTION: <detailed description of a professional, minimalistic image featuring two specific objects related to the theme>
# """
#
# category_generation_prompt = """
#     Generate 4 unique and relevant category names related to '{topic}' for a blog.
#     Each category name should be concise, use a maximum of two words, and should not include any numbers or special characters.
# """
#
#

keyword_research_prompt = """
You are an SEO specialist with expertise in content marketing. Generate a list of **5 unique, highly relevant, and trending keywords** for a blog about "{topic}".
- Each keyword must target high organic traffic potential and address user intent.
- Keywords must reflect current trends in searches.
- Avoid overly competitive terms or generic phrases.
"""

content_research_prompt = """
You are a skilled researcher and writer. Based on the provided keywords, gather information from **high-authority and reliable sources**.
- Create a casual and engaging summary that appeals to a younger audience.
- The summary must include **insights, practical examples, and unique perspectives**.
- Avoid references or links to other websites.
- The topic and subject should be relevant for the year {year}.
- Format the response as follows:
TITLE: Research Summary on {topic}
CONTENT: <detailed summary with 1000-1200 words>
"""

writing_prompt = """
Using the research provided, write a casual, relatable, and engaging article on the topic "{topic}".
- The topic and subject should be for the year {year}.
- Ensure the article is **original**, at least **1200 words** (target range: 1200-1500 words), and formatted in proper HTML structure for WordPress.
- Avoid passive voice; use active voice as much as possible.
- Include practical tips, relatable examples, and conversational language.
- Use a structure suitable for readability, with clear subtitles and short paragraphs.
- should use Casual and informal language and engaging tone to appeal to a younger audience.

Structure your response as follows:
TITLE: <fun and attention-grabbing title>
CONTENT:
<h1>Title of the Article</h1>
<p>Introduction: A fun and engaging opening that hooks the reader.</p>
<h2>Subtitle 1</h2>
<p>First main point: Casual discussion with practical insights.</p>
<h2>Subtitle 2</h2>
<p>Second main point: Relatable and actionable advice.</p>
<p>Conclusion: Wrap it up with a friendly tone and a call to action.</p>
"""

editing_prompt = """
You are an experienced editor. Review and improve the article provided below:
- Ensure the article is at least **1200 words** (expand sections if needed, adding actionable tips, relatable examples, or unique insights).
- Rewrite sentences to reduce passive voice (maximum 5% passive voice allowed).
- Break long sentences into concise, conversational statements (20 words or fewer per sentence).
- should use Casual and informal language and engaging tone to appeal to a younger audience.
- Structure the content for readability, using appropriate subtitles (with <h2>) and short paragraphs.
- Use HTML tags for formatting, like <b> for bold emphasis, but avoid references to other websites.

Return the revised article in this format:
TITLE: <refined title>
CONTENT:
<h1>Refined Title of the Article</h1>
<p>Introduction: Improved for flow and casual tone.</p>
<h2>Subtitle 1</h2>
<p>Body section 1: Simplified and engaging content.</p>
<h2>Subtitle 2</h2>
<p>Body section 2: Relatable and conversational content.</p>
<p>Conclusion: Clear, friendly wrap-up with no external references.</p>
CATEGORY: Select **one** item from the provided {categories} list that best matches the content theme.
IMAGE_DESCRIPTION: <detailed description of a fun, minimalistic image related to the theme>
"""

category_generation_prompt = """
Generate 4 unique and relevant category names related to '{topic}' for a blog.
Each category name should be concise, use a maximum of two words, and should not include any numbers or special characters.
"""

custom_editing_prompt = """
You are an experienced editor. Review and improve the article provided below:
- Ensure the article is at least **1200 words** (expand sections if needed, adding actionable tips, relatable examples, or unique insights).
- Rewrite sentences to reduce passive voice (maximum 5% passive voice allowed).
- Break long sentences into concise, conversational statements (20 words or fewer per sentence).
- Use casual and informal language and an engaging tone to appeal to a younger audience.
- Structure the content for readability, using appropriate subtitles (with <h2>) and short paragraphs.
- Format content with only <h1>, <h2>, and <p> tags, using <b> for emphasis when needed.
- Avoid external references or unnecessary metadata.

Do not include TITLE:, CATEGORY:, or IMAGE_DESCRIPTION: in the output.
"""