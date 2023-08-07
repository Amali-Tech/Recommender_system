import re
import numpy as np



def recommend(data, client_req, project_type, skill, rank, experience, cdc, internal, client):
    if project_type == 'Client':
      df = data[data['Client ready'] == 1]
    else:
      df = data

    static_cols = ['ID', 'Office', 'Name', 'Specialization', 'Rank', 'Position',
       'Previous Projects', 'Client ready',
       'Available for staffing \n (next 3m)', 'cdc_score', 'yrs_of_experience']


    df_cols = static_cols + client_req
    df = df[df_cols]

    # drop col with all empty req
    mask = df[client_req].isin(['-', np.nan]).all(axis=1)
    df = df[~mask]

    # Filtering based on availability
    df = df[df['Available for staffing \n (next 3m)'] == 1]
    

    df_new = df.reset_index(drop=True)
    df_new['Previous Projects'].fillna("", inplace = True)
    df = df_new
    


    internal_projects = ["ARMS", "iMocha", "Incident Management", "Event Management", "Image Detector", "Tourist Guide", 
                     "Booking Platform", "PMMD", "CV Builder", "Freelance", "Community Platform", "Virtual SaaS", "Market Place", "Payroll", "R&D", 
                     "Advent Calendar", "AmaliTech Website", "Chat App", "Commerce Cloud Upskilling",
                     "Nexum Scale-Up", "Nexum Scale-Up (Commerce Cloud)", "Nexum Scale-Up (Marketing Cloud)", "Nexum Scale-Up (StoryBlok)",
                     "Nexum Scale-up (Vue Storefront)", "Telekom upskilling"]
    

    for i in range(len(df)):
      projects = []

      # Total number of project
      if df.loc[i, "Previous Projects"] == "":
        df.loc[i, "total_projects_count"] = 0
      else:
        df.loc[i, "total_projects_count"] = len(df.loc[i, "Previous Projects"].split(","))

      # Number of internal projects
      for project in internal_projects:
          if(re.search(project, df.loc[i, "Previous Projects"], re.IGNORECASE)):
            projects.append(project)
    
      df.loc[i, "internal_projects_count"] = len(projects)

      # Number of client projects
      df.loc[i, "client_projects_count"] = df.loc[i, "total_projects_count"] - df.loc[i, "internal_projects_count"]

    
    


    # map skill levels to numerical represenation
    skill_mapping = {
          'Beginner': 1, 
          'Intermediate': 2,
          'Advanced': 3, 
          'Expert': 4}

    for req in client_req:
        df.loc[:, req] = df[req].map(skill_mapping)

    # Replace NaN or '-' with 0 in the specified columns
    df.loc[:, client_req] = df[client_req].fillna(0)

    # calc scores
    skill_multiplier = skill #3
    rank_multiplier = rank #2
    internal_mulitplier = internal #1
    client_multiplier = client #3
    experience_multiplier = experience #2
    cdc_multiplier = cdc #3


    df.loc[:, 'Skill Score'] = df[client_req].mul(skill_multiplier).sum(axis=1)
    df.loc[:, 'Rank Score'] = df['Rank'].mul(rank_multiplier)
    df.loc[:, 'Internal Project Score'] = df['internal_projects_count'].mul(internal_mulitplier)
    df.loc[:, 'Client Project Score'] = df['client_projects_count'].mul(client_multiplier)
    df.loc[:, 'Experience Score'] = df['yrs_of_experience'].mul(experience_multiplier)
    df.loc[:, 'CDC Score'] = df['cdc_score'].mul(cdc_multiplier)
    df.loc[:, 'Score'] = df['Skill Score'] + df['Rank Score'] + df['Internal Project Score'] + df['Client Project Score'] + df['Experience Score'].round(1) + df['CDC Score'].round(1)
    

    def level(row):
      if row == 1:
        return "Beginner"
      elif row == 2:
        return "Intermediate"
      elif row == 3:
        return "Advanced"
      elif row == 4:
        return "Expert"
      else:
        return "-"


    for req in client_req:
      df[req] = df[req].apply(level)

    def empty_projects(row):
      if row == "":
        return "-"
      else:
        return row


    df["Previous Projects"] = df["Previous Projects"].apply(empty_projects)



    output_columns = ["ID","Office", "Name", "Specialization", "Position", "Previous Projects"] + client_req + ["Score"]
    df = df.loc[:, output_columns]


    # Selecting Ideal and Nonideal Employees
    df_ideal = df.copy()
    df_nonideal = df.copy()


    df["Concat"] = ""
    for req in client_req:
      df["Concat"] += df[req]


    for i in range(len(df)):
      if re.search("-", df.loc[i, "Concat"], re.IGNORECASE):
        df_ideal = df_ideal.drop(i)
      else:
        df_nonideal = df_nonideal.drop(i)


    df_ideal = df_ideal.sort_values('Score', ascending=False, ignore_index=True).set_index("ID")
    df_nonideal = df_nonideal.sort_values('Score', ascending=False, ignore_index=True).set_index("ID")
    df = df.loc[:, output_columns].sort_values('Score', ascending=False, ignore_index=True).set_index("ID")



    return df_ideal, df_nonideal, df

