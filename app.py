from flask import Flask, render_template, request
import pandas as pd
import ast

app = Flask(__name__)

# Load the cluster_stats from the CSV
cluster_stats = pd.read_csv('sample_data.csv')

# Ensure that the Location column is a list for each cluster
# Convert the location column from string representation of lists to actual lists (if necessary)
cluster_stats['Location'] = cluster_stats['Location'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

# Get the unique locations (flattening the list of locations)
unique_locations = set([loc for sublist in cluster_stats['Location'] for loc in sublist])

# Function to determine the cluster based on age and location
def get_cluster(age, location):
    # Check if the provided location is in the list of unique locations
    if location not in unique_locations:
        return None  # Return None if location is not found

    # Find clusters where the average age is greater than or equal to the provided age
    matching_cluster = cluster_stats[cluster_stats['Avg_Age'] <= age]

    # Check if the location exists in any of the lists of locations for the clusters
    matching_cluster = matching_cluster[matching_cluster['Location'].apply(lambda loc_list: location in loc_list)]

    if not matching_cluster.empty:
        cluster = matching_cluster.iloc[0]
        return cluster
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print("POST request received")
        age = float(request.form['age'])
        location = request.form['location']

        # Get the cluster and book recommendations
        cluster = get_cluster(age, location)

        if cluster is not None:
            # Extract the recommended books and price/revenue
            recommended_books = cluster['Book_Titles']
            recommended_books = ast.literal_eval(recommended_books)
            # Debugging: Check the format of recommended_books
            #print("Recommended Books (Before Formatting):", recommended_books)

            # Ensure recommended_books is a list
            if isinstance(recommended_books, list):
                # Format it as a numbered list
                recommended_books = [f"{index + 1}. {book}" for index, book in enumerate(recommended_books)]

            else:
                # If it's a string (perhaps a single book or a long string), wrap it in a list
                recommended_books = [str(recommended_books)]

            # Debugging: Check the formatted recommended books list
            #print("Formatted Recommended Books:", recommended_books)


            # Prepare the results for rendering
            return render_template('result.html', books=recommended_books)
        else:
            return "No matching cluster found for the provided location and age."

    # If the request is a GET request, render the initial form with the unique locations
    return render_template('index.html', locations=sorted(list(unique_locations)))



 # Sort locations alphabetically

if __name__ == '__main__':
    app.run(debug=True)
