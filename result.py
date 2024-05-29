import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from math import pi

def show_result():
    # Load the user data from the CSV
    user_data = pd.read_csv('csv/user_data.csv')
    data_path = 'csv/data.csv'
    data = pd.read_csv(data_path)

    # Nearest Neighbor model to find top 5 closest grapes
    nn_model = NearestNeighbors(n_neighbors=5)
    nn_model.fit(data.drop('Druivensoort', axis=1))
    distances, indices = nn_model.kneighbors(user_data.drop('Druivensoort', axis=1))

    st.subheader("Top 5 Grape Recommendations")

    # Calculate the percentage match for the top 5 recommendations
    user_profile = user_data.drop('Druivensoort', axis=1).values
    top_grapes_indices = indices[0]
    top_grapes = data.iloc[top_grapes_indices]
    
    matches = []
    for index in top_grapes_indices:
        grape_profile = data.iloc[index].drop('Druivensoort').values.reshape(1, -1)
        match_score = cosine_similarity(user_profile, grape_profile)[0][0]
        match_percentage = round(match_score * 100, 2)
        matches.append((data.iloc[index]['Druivensoort'], match_percentage))

    # Display the top 5 recommendations with their match percentages
    match_df = pd.DataFrame(matches, columns=['Druivensoort', 'Match Percentage'])
    st.table(match_df)

    # K-Means clustering to find similar groups
    kmeans = KMeans(n_clusters=4, random_state=0).fit(data.drop('Druivensoort', axis=1))
    cluster_label = kmeans.predict(user_data.drop('Druivensoort', axis=1))
    cluster_data = data.iloc[kmeans.labels_ == cluster_label[0]]['Druivensoort']

    st.subheader("Similar Wines in Your Cluster")
    st.table(cluster_data)

    # Spider chart for visual comparison
    labels = data.columns[1:]
    stats_user = user_data.iloc[0, 1:].tolist()  # Exclude the name column
    stats_top1 = data.iloc[indices[0][0], 1:].tolist()  # Exclude the name column

    stats_user.append(stats_user[0])  # Close the loop for the radar chart
    stats_top1.append(stats_top1[0])  # Close the loop for the radar chart

    angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
    angles += [angles[0]]  # Close the loop for the angles

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    ax.plot(angles, stats_user, 'o-', linewidth=2, label='Your Preferences', color='green')
    ax.fill(angles, stats_user, color='green', alpha=0.25)
    ax.plot(angles, stats_top1, 'o-', linewidth=2, label='Top Match', color='blue')
    ax.fill(angles, stats_top1, color='blue', alpha=0.25)

    ax.set_thetagrids([a * 180 / pi for a in angles[:-1]], labels)
    ax.legend()
    st.pyplot(fig)
