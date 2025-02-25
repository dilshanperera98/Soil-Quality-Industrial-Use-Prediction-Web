import streamlit as st
import pickle
import pandas as pd
import base64

# Set page configuration
st.set_page_config(
    page_title="Soil Quality Predictor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for modern UI
st.markdown("""
<style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #388E3C;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    .st-expander {
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    h1, h2, h3 {
        color: #2E7D32;
        font-weight: 600;
    }
    .stSlider>div>div {
        background-color: #81C784;
    }
    .stAlert {
        border-radius: 8px;
    }
    .stSidebar .sidebar-content {
        background-color: #f1f8e9;
    }
    .prediction-card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
        border-left: 5px solid #4CAF50;
    }
    .sidebar-footer {
        position: fixed;
        bottom: 0;
        text-align: center;
        width: 100%;
        padding: 10px;
        background-color: #e8f5e9;
        border-top: 1px solid #c8e6c9;
    }
    .nav-item {
        margin-bottom: 8px;
        padding: 10px;
        border-radius: 8px;
        transition: background-color 0.3s;
    }
    .nav-item:hover {
        background-color: #e8f5e9;
    }
</style>
""", unsafe_allow_html=True)

# Load models
with open("rf_soil_quality_model.pkl", "rb") as f:
    rf_soil_quality = pickle.load(f)

with open("rf_industrial_use_model.pkl", "rb") as f:
    rf_industrial_use = pickle.load(f)

with open("rf_soil_quality_model_LG.pkl", "rb") as f:
    rf_soil_quality_LG = pickle.load(f)

with open("rf_industrial_use_model_LG.pkl", "rb") as f:
    rf_industrial_use_LG = pickle.load(f)

# Define mappings
soil_quality_mapping = {0: "Poor", 1: "Moderate", 2: "Good"}
industrial_use_mapping = {0: "Agriculture", 1: "Construction", 2: "Landscaping"}

# Sidebar Navigation with icons
st.sidebar.markdown("<h2 style='text-align: center; color: #2E7D32;'>🌱 Soil Quality Predictor</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<div style='height: 2px; background: #e0e0e0; margin-bottom: 20px;'></div>", unsafe_allow_html=True)

pages = {
    "Home": "🏠",
    "About Us": "👥",
    "Predict [RandomForest]": "🔍",
    "Predict [Logistic Regression]": "📊",
    "Resources": "📚"
}

# Create fancy navigation buttons
for page_name, icon in pages.items():
    if st.sidebar.markdown(f"""
    <div class='nav-item' onclick='this.style.backgroundColor="#c8e6c9"'>
        <a href='#' style='text-decoration: none; color: #333; font-weight: 500;'>{icon} {page_name}</a>
    </div>
    """, unsafe_allow_html=True):
        page = page_name

page = st.sidebar.radio("", list(pages.keys()), format_func=lambda x: f"{pages[x]} {x}", label_visibility="collapsed")

# Footer
st.sidebar.markdown(
    """
    <div class='sidebar-footer'>
        <div style='text-align: center; color: #2E7D32;'>
            Powered by AI 🤖
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

if page == "Home":
    st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'>Welcome to Soil Quality & Industrial Use Prediction</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #2E7D32;'>Smart Soil Analysis</h3>
            <p style='font-size: 16px; line-height: 1.6;'>
                This AI-powered app predicts soil quality and its potential industrial use based on key parameters such as texture, 
                moisture, organic matter, pH, and electrical conductivity.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #2E7D32;'>📌 How It Works:</h3>
            <ol style='font-size: 16px; line-height: 1.8;'>
                <li>Navigate to the <b>Predict</b> page using the sidebar navigation.</li>
                <li>Enter the required soil parameters in the interactive form.</li>
                <li>Click <b>Predict</b> to get instant quality and industrial use predictions.</li>
            </ol>
            <p style='font-weight: 500; color: #2E7D32; margin-top: 15px;'>Let's get started! 🚀</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; height: 100%; display: flex; flex-direction: column; justify-content: center; text-align: center;'>
            <h2 style='color: #2E7D32;'>Why Use Our Tool?</h2>
            <div style='margin: 15px 0; padding: 15px; background-color: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
                <h4 style='color: #2E7D32;'>🎯 High Accuracy</h4>
                <p>Random Forest model with 99% accuracy</p>
            </div>
            <div style='margin: 15px 0; padding: 15px; background-color: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
                <h4 style='color: #2E7D32;'>⚡ Instant Results</h4>
                <p>Get predictions in seconds</p>
            </div>
            <div style='margin: 15px 0; padding: 15px; background-color: white; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
                <h4 style='color: #2E7D32;'>🔄 Multiple Models</h4>
                <p>Compare different prediction approaches</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "About Us":
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>📖 About Us</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("""
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #2E7D32;'>Who We Are</h3>
            <p style='font-size: 16px; line-height: 1.6;'>
                We are a team of soil scientists and data engineers who developed this app to help farmers, 
                agronomists, and industrialists understand the soil quality and its potential uses in different sectors.
            </p>
            <p style='font-size: 16px; line-height: 1.6;'>
                Our mission is to provide reliable AI-driven predictions for optimal soil management and industrial use.
            </p>
        </div>
        
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 20px;'>
            <h3 style='color: #2E7D32;'>Our Goal</h3>
            <p style='font-size: 16px; line-height: 1.6;'>
                To empower industries and agriculture with insights on soil quality and its 
                suitability for different industrial uses.
            </p>
        </div>
        
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 20px;'>
            <h3 style='color: #2E7D32;'>Real-World Impact</h3>
            <p style='font-size: 16px; line-height: 1.6;'>
                This app has already helped several farmers optimize soil management practices, reduce costs, and enhance productivity. 
                We're constantly working to improve the accuracy of our models and add new features that will help a wider range of industries.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='background-color: #e8f5e9; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
            <h3 style='color: #2E7D32; text-align: center;'>Contact Us</h3>
            <p style='font-size: 16px; line-height: 1.6; text-align: center;'>
                We value your feedback! Feel free to reach out to us for any inquiries or suggestions.
            </p>
            <div style='text-align: center; margin-top: 20px;'>
                <a href='mailto:contact@soilpredictions.com' style='text-decoration: none;'>
                    <div style='background-color: white; padding: 10px 15px; border-radius: 30px; display: inline-block; margin: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                        <span style='color: #2E7D32;'>✉️ Email Us</span>
                    </div>
                </a>
            </div>
            <div style='text-align: center; margin-top: 10px;'>
                <a href='https://www.linkedin.com/' style='text-decoration: none;'>
                    <div style='background-color: white; padding: 10px 15px; border-radius: 30px; display: inline-block; margin: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                        <span style='color: #2E7D32;'>LinkedIn</span>
                    </div>
                </a>
                <a href='https://twitter.com/' style='text-decoration: none;'>
                    <div style='background-color: white; padding: 10px 15px; border-radius: 30px; display: inline-block; margin: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                        <span style='color: #2E7D32;'>Twitter</span>
                    </div>
                </a>
            </div>
        </div>
        
        <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin-top: 20px;'>
            <h3 style='color: #2E7D32; text-align: center;'>Our Team</h3>
            <div style='display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-top: 15px;'>
                <div style='text-align: center;'>
                    <div style='width: 60px; height: 60px; background-color: #c8e6c9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;'>
                        <span style='font-size: 24px;'>👩‍🔬</span>
                    </div>
                    <p style='margin-top: 5px; font-weight: 500;'>Dr. Soil</p>
                    <p style='font-size: 12px; color: #666;'>Lead Scientist</p>
                </div>
                <div style='text-align: center;'>
                    <div style='width: 60px; height: 60px; background-color: #c8e6c9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;'>
                        <span style='font-size: 24px;'>👨‍💻</span>
                    </div>
                    <p style='margin-top: 5px; font-weight: 500;'>Data Pro</p>
                    <p style='font-size: 12px; color: #666;'>ML Engineer</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif page == "Predict [RandomForest]":
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🔍 Soil Quality & Industrial Use Prediction</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #f1f8e9; padding: 15px; border-radius: 10px; border-left: 5px solid #4CAF50; margin-bottom: 20px;'>
        <p style='font-size: 16px; margin: 0;'>📍 The Random Forest model achieves a <b>99% accuracy level</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 16px;'>Enter soil parameters below to predict its quality and industrial usability.</p>", unsafe_allow_html=True)
    
    # Create a card-like container for the form
    st.markdown("""
    <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
    """, unsafe_allow_html=True)
    
    # Input fields
    texture_options = {"Clayey": 0, "Sandy": 1, "Sandy Loam": 2, "Loamy": 3}
    col1, col2 = st.columns(2)
    
    with col1:
        texture = st.selectbox("Select Texture Type:", list(texture_options.keys()))
        texture_input = texture_options[texture]
        moisture_input = st.slider("Moisture (%)", 0.0, 100.0, 20.0)
        organic_matter_input = st.slider("Organic Matter (%)", 0.0, 10.0, 2.5)
    
    with col2:
        ph_input = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1)
        conductivity_input = st.number_input("Electrical Conductivity (dS/m)", min_value=0.0, max_value=10.0, value=1.0, step=0.1)
    
    # Close card container
    st.markdown("</div>", unsafe_allow_html=True)

    # Prediction function
    def predict_soil_quality_industrial_use(texture, moisture, organic_matter, ph, conductivity):
        input_data = pd.DataFrame([[texture, moisture, organic_matter, ph, conductivity]],
                                 columns=['Texture', 'Moisture (%)', 'Organic Matter (%)', 'pH', 'Electrical Conductivity (dS/m)'])
        soil_quality_pred = rf_soil_quality.predict(input_data)[0]
        industrial_use_pred = rf_industrial_use.predict(input_data)[0]
        return soil_quality_mapping.get(soil_quality_pred, "Unknown"), industrial_use_mapping.get(industrial_use_pred, "Unknown")

    # Center the predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("Predict", key="rf_predict")

    # Predict button handling
    if predict_button:
        soil_quality, industrial_use = predict_soil_quality_industrial_use(texture_input, moisture_input, organic_matter_input, ph_input, conductivity_input)
        
        # Display results in a modern card layout
        st.markdown("""
        <div class='prediction-card'>
            <h2 style='text-align: center; color: #2E7D32; margin-bottom: 20px;'>Prediction Results</h2>
            <div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>
                <div style='background-color: #e8f5e9; padding: 20px; border-radius: 10px; text-align: center; flex: 1; min-width: 200px;'>
                    <h3 style='color: #2E7D32; margin-bottom: 10px;'>Soil Quality</h3>
                    <div style='font-size: 24px; font-weight: bold; color: #1B5E20;'>%s</div>
                    <div style='margin-top: 10px; font-size: 40px;'>🌱</div>
                </div>
                <div style='background-color: #e3f2fd; padding: 20px; border-radius: 10px; text-align: center; flex: 1; min-width: 200px;'>
                    <h3 style='color: #0D47A1; margin-bottom: 10px;'>Industrial Use</h3>
                    <div style='font-size: 24px; font-weight: bold; color: #0D47A1;'>%s</div>
                    <div style='margin-top: 10px; font-size: 40px;'>🏗️</div>
                </div>
            </div>
        </div>
        """ % (soil_quality, industrial_use), unsafe_allow_html=True)

elif page == "Predict [Logistic Regression]":
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🔍 Soil Quality & Industrial Use Prediction</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 5px solid #ff9800; margin-bottom: 20px;'>
        <p style='font-size: 16px; margin: 0;'>📍 The Logistic Regression model achieves a <b>72% accuracy level</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<p style='font-size: 16px;'>Enter soil parameters below to predict its quality and industrial usability.</p>", unsafe_allow_html=True)
    
    # Create a card-like container for the form
    st.markdown("""
    <div style='background-color: white; padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);'>
    """, unsafe_allow_html=True)
    
    # Input fields
    texture_options = {"Clayey": 0, "Sandy": 1, "Sandy Loam": 2, "Loamy": 3}
    col1, col2 = st.columns(2)
    
    with col1:
        texture = st.selectbox("Select Texture Type:", list(texture_options.keys()))
        texture_input = texture_options[texture]
        moisture_input = st.slider("Moisture (%)", 0.0, 100.0, 20.0, key="lg_moisture")
        organic_matter_input = st.slider("Organic Matter (%)", 0.0, 10.0, 2.5, key="lg_organic")
    
    with col2:
        ph_input = st.number_input("pH", min_value=0.0, max_value=14.0, value=7.0, step=0.1, key="lg_ph")
        conductivity_input = st.number_input("Electrical Conductivity (dS/m)", min_value=0.0, max_value=10.0, value=1.0, step=0.1, key="lg_cond")
    
    # Close card container
    st.markdown("</div>", unsafe_allow_html=True)

    # Prediction function
    def predict_soil_quality_industrial_use(texture, moisture, organic_matter, ph, conductivity):
        input_data = pd.DataFrame([[texture, moisture, organic_matter, ph, conductivity]],
                               columns=['Texture', 'Moisture (%)', 'Organic Matter (%)', 'pH', 'Electrical Conductivity (dS/m)'])
        soil_quality_pred = rf_soil_quality_LG.predict(input_data)[0]
        industrial_use_pred = rf_industrial_use_LG.predict(input_data)[0]
        return soil_quality_mapping.get(soil_quality_pred, "Unknown"), industrial_use_mapping.get(industrial_use_pred, "Unknown")

    # Center the predict button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("Predict", key="lg_predict")

    # Predict button handling
    if predict_button:
        soil_quality, industrial_use = predict_soil_quality_industrial_use(texture_input, moisture_input, organic_matter_input, ph_input, conductivity_input)
        
        # Display results in a modern card layout with different colors for LG model
        st.markdown("""
        <div class='prediction-card' style='border-left: 5px solid #ff9800;'>
            <h2 style='text-align: center; color: #e65100; margin-bottom: 20px;'>Prediction Results</h2>
            <div style='display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;'>
                <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px; text-align: center; flex: 1; min-width: 200px;'>
                    <h3 style='color: #e65100; margin-bottom: 10px;'>Soil Quality</h3>
                    <div style='font-size: 24px; font-weight: bold; color: #e65100;'>%s</div>
                    <div style='margin-top: 10px; font-size: 40px;'>🌱</div>
                </div>
                <div style='background-color: #fff3e0; padding: 20px; border-radius: 10px; text-align: center; flex: 1; min-width: 200px;'>
                    <h3 style='color: #e65100; margin-bottom: 10px;'>Industrial Use</h3>
                    <div style='font-size: 24px; font-weight: bold; color: #e65100;'>%s</div>
                    <div style='margin-top: 10px; font-size: 40px;'>🏗️</div>
                </div>
            </div>
        </div>
        """ % (soil_quality, industrial_use), unsafe_allow_html=True)

elif page == "Resources":
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>📚 Learning About Soils</h1>", unsafe_allow_html=True)
    
    # Modern styled expanders
    with st.expander("Introduction to Soil Science"):
        st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
            <h3 style='color: #2E7D32;'>Definition of Soil</h3>
            <p style='font-size: 15px; line-height: 1.6;'>
                Soil is a natural resource that forms on the Earth's surface. It consists of mineral particles, 
                organic matter, water, and air. Soil is crucial for plant growth, water filtration, and supporting ecosystems.
            </p>
            
            <h3 style='color: #2E7D32; margin-top: 20px;'>Importance of Soil</h3>
            <p style='font-size: 15px; line-height: 1.6;'>
                Soil provides nutrients, water retention, and mechanical support for plants. It also serves as a habitat for 
                diverse organisms, plays a vital role in carbon sequestration, and helps filter water.
            </p>
            
            <h3 style='color: #2E7D32; margin-top: 20px;'>Soil and Ecosystem Balance</h3>
            <p style='font-size: 15px; line-height: 1.6;'>
                Healthy soil maintains the balance of various ecosystems, sustaining plant life and contributing to biodiversity.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Key Soil Properties"):
        st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
            <div style='display: flex; flex-wrap: wrap; gap: 20px;'>
                <div style='flex: 1; min-width: 250px;'>
                    <h3 style='color: #2E7D32;'>Soil Texture</h3>
                    <p style='font-size: 15px; line-height: 1.6;'>
                        Soil texture refers to the proportion of sand, silt, and clay in the soil. It determines how water and 
                        air move through the soil and affects plant growth.
                    </p>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <h3 style='color: #2E7D32;'>pH Levels</h3>
                    <p style='font-size: 15px; line-height: 1.6;'>
                        Soil pH influences nutrient availability for plants. Most plants thrive in neutral to slightly acidic soils (pH 6-7).
                    </p>
                </div>
            </div>
            
            <div style='display: flex; flex-wrap: wrap; gap: 20px; margin-top: 20px;'>
                <div style='flex: 1; min-width: 250px;'>
                    <h3 style='color: #2E7D32;'>Organic Matter</h3>
                    <p style='font-size: 15px; line-height: 1.6;'>
                        The decayed remains of plants and animals. Organic matter improves soil structure, 
                        moisture retention, and nutrient content.
                    </p>
                </div>
                <div style='flex: 1; min-width: 250px;'>
                    <h3 style='color: #2E7D32;'>Soil Moisture</h3>
                    <p style='font-size: 15px; line-height: 1.6;'>
                        The amount of water present in the soil is essential for plant growth. Proper moisture levels promote healthy crops.
                    </p>
                </div>
            </div>
            
            <div style='margin-top: 20px;'>
                <h3 style='color: #2E7D32;'>Electrical Conductivity</h3>
                <p style='font-size: 15px; line-height: 1.6;'>
                    Indicates the level of salts and minerals in the soil, which can affect plant growth if too high.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Types of Soil"):
        st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);'>
            <div style='display: flex; flex-wrap: wrap; gap: 20px;'>
                <div style='flex: 1; min-width: 200px; background-color: #f8f9fa; padding: 15px; border-radius: 8px;'>
                    <h3 style='color: #2E7D32;'>Clay Soil</h3>
                    <p style='font-size: 15px; line-height: 1.6;'>
                        Clay particles are small and dense, which makes the soil sticky when wet. It is nutrient-rich but poorly drained.
                    </p>
                </div>
                <div style='flex: 1; min-width: 200px; background-color: #f8f9fa; padding: 15px
                """
                )
                