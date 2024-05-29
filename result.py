import streamlit as st
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from math import pi
import io

def send_email(receiver_address, subject, body, plot_img):
    sender_address = st.secrets["email"]["sender"]
    sender_pass = st.secrets["email"]["app_password"]  # Use the App Password here
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # TLS
    
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_address, sender_pass)
    
    message = MIMEMultipart("related")
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject

    message.attach(MIMEText(body, 'html'))

    img = MIMEImage(plot_img.getvalue())
    img.add_header('Content-ID', '<plot>')
    message.attach(img)

    server.send_message(message)
    server.quit()


def show_result():
    user_data = pd.read_csv('csv/user_data.csv')
    data_path = 'csv/data.csv'
    data = pd.read_csv(data_path)
    nn_model = NearestNeighbors(n_neighbors=5)
    nn_model.fit(data.drop('Druivensoort', axis=1))
    distances, indices = nn_model.kneighbors(user_data.drop('Druivensoort', axis=1))

    st.subheader("Top 5 druif aanbevelingen")
    user_profile = user_data.drop('Druivensoort', axis=1).values
    top_grapes_indices = indices[0]
    top_grapes = data.iloc[top_grapes_indices]
    
    matches = []
    for index in top_grapes_indices:
        grape_profile = data.iloc[index].drop('Druivensoort').values.reshape(1, -1)
        match_score = cosine_similarity(user_profile, grape_profile)[0][0]
        match_percentage = round(match_score * 100, 2)
        matches.append((data.iloc[index]['Druivensoort'], match_percentage))

    match_df = pd.DataFrame(matches, columns=['Druivensoort', 'Match Percentage'])
    st.table(match_df)

    kmeans = KMeans(n_clusters=4, random_state=0).fit(data.drop('Druivensoort', axis=1))
    cluster_label = kmeans.predict(user_data.drop('Druivensoort', axis=1))
    cluster_data = data.iloc[kmeans.labels_ == cluster_label[0]]['Druivensoort']
    cluster_df = pd.DataFrame(cluster_data)
    st.subheader("Vergelijkbare druiven")
    st.table(cluster_data)

    labels = data.columns[1:]
    stats_user = user_data.iloc[0, 1:].tolist()
    stats_top1 = data.iloc[indices[0][0], 1:].tolist()

    stats_user.append(stats_user[0])
    stats_top1.append(stats_top1[0])

    angles = [n / float(len(labels)) * 2 * pi for n in range(len(labels))]
    angles += [angles[0]]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.plot(angles, stats_user, 'o-', linewidth=2, label='Uw voorkeuren', color='green')
    ax.fill(angles, stats_user, color='green', alpha=0.25)
    ax.plot(angles, stats_top1, 'o-', linewidth=2, label='Top Match', color='blue')
    ax.fill(angles, stats_top1, color='blue', alpha=0.25)
    ax.set_thetagrids([a * 180 / pi for a in angles[:-1]], labels)
    ax.legend()
    st.pyplot(fig)

    # Save plot to a BytesIO buffer
    plot_buffer = io.BytesIO()
    fig.savefig(plot_buffer, format='png')
    plot_buffer.seek(0)

    email = st.text_input("Wat is uw e-mailadres?")
    if st.button("Verzend resultaat."):
        html_content = f"<html><body><p>Hier zijn uw top 5 aanbevolen druif soorten:</p>{match_df.to_html(index=False)}<br><p>Vergelijkbare druiven:</p>{cluster_df.to_html(index=False)}<br><img src='cid:plot' alt='Graph'></body></html>"
        send_email(email, "Uw druif aanbeveling.", html_content, plot_buffer)
