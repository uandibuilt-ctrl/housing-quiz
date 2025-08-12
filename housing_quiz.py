import streamlit as st

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")
st.markdown("*Not official advice. Always verify with government sites.*")

with st.form(key="quiz_form"):
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)
    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))
    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))
    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))
    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)
    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))
    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)
    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)
    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))
    submit = st.form_submit_button("Submit and Assess")

if submit:
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")
    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")
st.markdown("*Not official advice. Always verify with government sites.*")

with st.form(key="quiz_form"):
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)
    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))
    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))
    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))
    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)
    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))
    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)
    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)
    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))
    submit = st.form_submit_button("Submit and Assess")

if submit:
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")
    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")
st.markdown("*Not official advice. Always verify with government sites.*")

with st.form(key="quiz_form"):
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)
    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))
    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))
    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))
    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)
    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))
    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)
    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)
    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))
    submit = st.form_submit_button("Submit and Assess")

if submit:
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")
    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")
st.markdown("*Not official advice. Always verify with government sites.*")

with st.form(key="quiz_form"):
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)
    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))
    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))
    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))
    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)
    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))
    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)
    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)
    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))
    submit = st.form_submit_button("Submit and Assess")

if submit:
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")
    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")
st.markdown("*Not official advice. Always verify with government sites.*")

with st.form(key="quiz_form"):
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)
    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))
    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))
    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))
    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)
    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))
    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)
    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)
    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))
    submit = st.form_submit_button("Submit and Assess")

if submit:
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")
    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")

with st.form(key="quiz_form"):
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)
    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))
    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))
    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))
    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)
    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))
    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)
    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)
    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))
    submit = st.form_submit_button("Submit and Assess")

if submit:
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")
    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")

# Prototype converted to Streamlit App: Australian Public Housing Eligibility Quiz (2025 Edition)
# This is a basic simulation - not official. Always check government sites for latest.

st.title("Aussie Public Housing Eligibility Quiz")
st.write("Answer the questions to get a quick assessment. Based on 2025 rules. Helps navigate red tape.")
st.write("Note: Eligibility varies by state/territory.")

# Use a form to collect all inputs at once
with st.form(key="quiz_form"):
    # Supported states
    states = ["NSW", "VIC", "QLD", "SA", "WA", "TAS", "NT", "ACT"]
    state = st.selectbox("Which state/territory are you applying in?", states)

    citizenship = st.radio("Are you an Australian citizen or permanent resident?", ("Yes", "No"))

    state_resident = st.radio(f"Are you a resident of {state}?", ("Yes", "No"))

    owns_property = st.radio("Do you own or partly own any property in Australia?", ("Yes", "No"))

    household_size = st.number_input("How many people in your household (including yourself)?", min_value=1, step=1)

    has_independent_income = st.radio("Does at least one household member have an independent income?", ("Yes", "No"))

    st.write("Income limits are weekly gross before tax. Assets exclude super but include cash/savings.")
    income = st.number_input("What's your household's total weekly gross income? (e.g., 800)", min_value=0.0, step=1.0)

    assets = st.number_input("What's your household's total assessable assets? (e.g., 5000)", min_value=0.0, step=1.0)

    priority = st.radio("Do you have priority needs? (e.g., homelessness, disability, domestic violence)", ("Yes", "No"))

    submit = st.form_submit_button("Submit and Assess")

if submit:
    # Process eligibility (same logic as prototype)
    eligible = True
    notes = []

    if citizenship == "No":
        eligible = False
        notes.append("You must be an Australian citizen or permanent resident to be eligible.")
    elif state_resident == "No":
        eligible = False
        notes.append(f"You need to be a {state} resident to apply here.")
    elif owns_property == "Yes":
        eligible = False
        notes.append("Property owners are generally ineligible.")

    # State-Specific Income and Asset Limits (2025 Data) - Same as your prototype
    if state == "NSW":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38000 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "VIC":
        income_limit = 1157 if household_size == 1 else 1769 if household_size == 2 else 1769 + (household_size - 2) * 617
        asset_limit = 22998
    elif state == "QLD":
        income_limit = 609 if household_size == 1 else 742 if household_size == 2 else 742 + (household_size - 2) * 133
        asset_limit = 122875 if household_size == 1 else 147875 if household_size == 2 else 172875
        if has_independent_income == "No":
            eligible = False
            notes.append("QLD requires at least one applicant with independent income.")
    elif state == "SA":
        income_limit = 869 if household_size == 1 else 1062 if household_size == 2 else 1062 + (household_size - 2) * 193
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "WA":
        income_limit = 606 if household_size == 1 else 808 if household_size == 2 else 808 + (household_size - 2) * 202
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "TAS":
        income_limit = 780 if household_size == 1 else 1075 if household_size == 2 else 1075 + (household_size - 2) * 295
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "NT":
        income_limit = 800 if household_size == 1 else 1100 if household_size == 2 else 1100 + (household_size - 2) * 300
        asset_limit = 38400 if household_size == 1 else 63800 if household_size == 2 else 89000
    elif state == "ACT":
        income_limit = 887 if household_size == 1 else 1109 if household_size == 2 else 1109 + (household_size - 2) * 148
        asset_limit = 40000

    if income > income_limit:
        eligible = False
        notes.append(f"Income exceeds {state} limit of ~${income_limit}/week for {household_size} people.")
    if assets > asset_limit:
        eligible = False
        notes.append(f"Assets exceed {state} limit of ~${asset_limit}.")

    if priority == "Yes":
        notes.append("You may qualify for priority access, reducing wait times.")

    # Wait Time Estimator (same as prototype)
    priority_wait = {
        "NSW": "1-2 years", "VIC": "18-20 months", "QLD": "21-28 months", "SA": "1-3 years",
        "WA": "2-3 years", "TAS": "1-2 years", "NT": "5-8 years", "ACT": "1-2 years"
    }
    general_wait = {
        "NSW": "5-10 years", "VIC": "3-5 years", "QLD": "3-5 years", "SA": "3-5 years",
        "WA": "3-5 years", "TAS": "2-3 years", "NT": "8-10 years", "ACT": "3-5 years"
    }
    wait_estimate = priority_wait[state] if priority == "Yes" else general_wait[state]

    # Display Results
    st.subheader("Assessment")
    if eligible:
        st.success("Based on your answers, you may be eligible! Apply soon to join the waitlist.")
    else:
        st.error("You may not be eligible due to:")
        for note in notes:
            st.write(f"- {note}")

    st.write(f"Estimated wait time in {state}: {wait_estimate} (varies by location and demand; check official reports).")

    st.subheader("Next Steps Without Red Tape")
    st.write("1. Gather docs: ID, income proof, Centrelink statements.")
    st.write("2. Apply online:")

    apply_links = {
        "NSW": "https://www.facs.nsw.gov.au/housing/apply",
        "VIC": "https://www.housing.vic.gov.au/apply-social-housing",
        "QLD": "https://www.qld.gov.au/housing/public-community-housing/apply",
        "SA": "https://housing.sa.gov.au/services/public-housing/apply-for-housing",
        "WA": "https://www.wa.gov.au/service/housing-and-property/public-housing/apply-public-housing",
        "TAS": "https://www.homestasmania.com.au/Apply-for-Housing",
        "NT": "https://nt.gov.au/property/social-housing/apply-for-housing/apply-for-public-housing",
        "ACT": "https://www.act.gov.au/housing-planning-and-property/public-housing/apply-for-housing"
    }
    st.write(f"- {apply_links[state]}")
    st.write("3. For full national info: https://my.gov.au/en/services/living-arrangements/finding-renting-and-buying-a-home/help-with-homelessness/social-public-and-community-housing")
    st.write("4. If stuck, contact a housing support service like 1800 825 955 (national homelessness hotline).")







