import streamlit as st
import google.generativeai as genai
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Content Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Color Scheme and Enhanced CSS
st.markdown("""
    <style>
        /* Main theme colors */
        :root {
            --primary-color: #7C3AED;
            --secondary-color: #4F46E5;
            --accent-color: #F472B6;
            --background-color: #F3F4F6;
            --text-color: #1F2937;
            --success-color: #10B981;
            --error-color: #EF4444;
        }

        /* Global styles */
        .main {
            padding: 2rem;
            background-color: var(--background-color);
        }

        /* Card-like containers */
        .stCard {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
        }

        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 8px;
            height: 3.5em;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            border: none;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
        }

        /* Input fields */
        .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>select {
            background-color: white;
            border: 2px solid #E5E7EB;
            border-radius: 8px;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }
        .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.2);
        }

        /* Headers */
        h1 {
            color: var(--primary-color);
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 2rem;
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        h2, h3 {
            color: var(--text-color);
            margin-bottom: 1rem;
        }

        /* Sidebar */
        .css-1d391kg {
            background-color: white;
            padding: 2rem 1rem;
        }

        /* Status messages */
        .success-box {
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--success-color);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        .error-box {
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--error-color);
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }

        /* Feature boxes in sidebar */
        .feature-box {
            background-color: #F9FAFB;
            border-left: 4px solid var(--primary-color);
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0 8px 8px 0;
        }

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 1rem;
        }
        .stTabs [data-baseweb="tab"] {
            height: 3rem;
            border-radius: 8px;
            padding: 0 1rem;
            font-weight: 500;
        }

        /* Progress bars */
        .stProgress > div > div > div > div {
            background-color: var(--primary-color);
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_blogs' not in st.session_state:
    st.session_state.generated_blogs = []

def generate_blog(topic, description, keywords,word_count, tone, target_audience, content_type):
    prompt = f"""
    You are an expert {content_type} writer specializing in SEO-driven content. Your task is to craft a compelling, well-structured, and highly engaging piece that aligns with the provided specifications.

    ## Content Specifications:
    - **Topic:** {topic}
    - **Primary and Secondary Keywords:** {keywords}
    - **Target Word Count:** {word_count}
    - **Tone & Style:** {tone}
    - **Target Audience:** {target_audience}

    ## Writing Guidelines:
    1. **Headings & Structure**  
    - Use a **clear and logical heading hierarchy** (# for H1, ## for H2, ### for H3).  
    - Each major section (H2) must have **at least two well-developed subsections** (H3).  
    - Ensure all headings are **descriptive and informative** to improve readability and SEO.

    2. **Engagement & Readability**  
    - Open with a **strong, attention-grabbing introduction** (2-3 paragraphs).  
    - Maintain a **smooth narrative flow** with natural transitions between sections.  
    - Write in **short, digestible paragraphs** that enhance readability.  
    - Use **rich, vivid language** while keeping the content professional and informative.  

    3. **SEO Optimization**  
    - Naturally **incorporate target keywords** throughout the content without keyword stuffing.  
    - Use **semantic variations** and related terms to enhance search relevance.  
    - Structure content for **featured snippets** (concise, direct answers in key sections).  

    4. **Content Structure:**  
    1. **Title (H1):** A compelling, SEO-friendly title.  
    2. **Introduction:** Engaging overview (2-3 paragraphs).  
    3. **Main Sections (H2):**  
        - Each section should have at least **two** well-developed subsections (H3).  
        - Each subsection should contain **2-3 in-depth paragraphs** with smooth transitions.  
    4. **Conclusion:** A strong closing statement (1-2 paragraphs), summarizing key takeaways.  

    ## Formatting & Style Rules:
    - **Use proper Markdown syntax** for headings.  
    - **Do NOT use bullet points** (except within this guideline).  
    - **Maintain consistent paragraph spacing** for readability.  
    - **Avoid fluff**—every sentence should add value.  
    - **No external/internal link suggestions, meta descriptions, or author bios.**  

    Your goal is to deliver **polished, high-quality content** that is both engaging for readers and optimized for search engines.
    """

    
    if description:
        prompt += f"\n\nAdditional Context:\n{description}"

    try:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt, stream=True)

        blog_content = ""
        blog_placeholder = st.empty()

        for chunk in response:
            if chunk.text:
                blog_content += chunk.text
                blog_placeholder.markdown(blog_content)

        return blog_content
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

def main():
    st.title("✨ AI Content Generator Pro")

    # Enhanced Sidebar with Description
    with st.sidebar:
        st.markdown("### 🎯 About")
        st.markdown("""
        The AI Content Generator Pro helps you create high-quality, SEO-optimized content with ease. 
        Perfect for content creators, marketers, and business owners.
        """)
        
        st.markdown("### ✨ Key Features")
        features = [
            "🎨 Multiple content types support",
            "🎯 Audience-targeted content",
            "📝 Customizable tone and style",
            "📱 Mobile-friendly formatting",
            "🔄 Real-time generation"
        ]
        for feature in features:
            st.markdown(f"""
            <div class="feature-box">
                {feature}
            </div>
            """, unsafe_allow_html=True)

    # Main content area
    with st.container():
        # Content Type Selection
        col1, col2 = st.columns([1, 2])
        with col1:
            content_type = st.selectbox(
                "Select Content Type",
                ["Blog Post", "Article", "Product Description", "Social Media Post", "Newsletter"],
                index=0
            )

        # Main input form
        with st.expander("✍️ Content Details", expanded=True):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                topic = st.text_input("Topic", placeholder="Enter your main topic...")
                keywords = st.text_input("Keywords", placeholder="Enter comma-separated keywords...")
                description = st.text_area("Description (Optional)", 
                                         placeholder="Add any additional details or specific requirements...",
                                         help="Optional: Provide more context or specific requirements")

            with col2:
                # Changed from slider to selectbox
                tone = st.selectbox(
                    "Content Tone",
                    ["Casual", "Conversational", "Professional", "Technical", "Formal"],
                    index=2
                )
                # Changed from slider to selectbox
                target_audience = st.selectbox(
                    "Target Audience",
                    ["Beginner", "Intermediate", "Advanced", "Expert"],
                    index=1
                )
                word_count = st.slider("Word Count", 300, 2000, 500, 50,
                                     help="Adjust the length of your content")

        # Generation Controls
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            generate_btn = st.button("🚀 Generate Content")

        if generate_btn:
            if topic and keywords:
                with st.spinner("✨ Creating your content..."):
                    blog_content = generate_blog(topic, description, keywords,
                                              word_count, tone, target_audience, content_type)
                    
                    if blog_content:
                        st.success("✅ Content generated successfully!")
                        
                        # Store in session state
                        st.session_state.generated_blogs.append({
                            'topic': topic,
                            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'content': blog_content
                        })
                        
                        # Download options
                        st.download_button(
                            "📥 Download Markdown",
                            blog_content,
                            file_name=f"content_{datetime.now().strftime('%Y%m%d')}.md",
                            mime="text/markdown"
                        )

            else:
                st.warning("⚠️ Please fill in all required fields (Topic, Keywords, and Author)")

if __name__ == "__main__":
    main()