// Deterministic mock data generator to match the Vehicle Insurance Fraud Data dashboard statistics exactly
const generateMockClaims = () => {
  const states = ['OH', 'IN', 'IL'];
  const incidentTypes = ['Single Vehicle Collision', 'Multi-vehicle Collision', 'Vehicle Theft', 'Parked Car'];
  const severities = ['Minor Damage', 'Major Damage', 'Total Loss', 'Trivial Damage'];
  const collisionTypes = ['Front Collision', 'Rear Collision', 'Side Collision', 'Unknown'];
  const educations = ['High School', 'College', 'Associate', 'Masters', 'JD', 'MD', 'PhD'];
  const hobbies = ['reading', 'chess', 'yachting', 'skydiving', 'camping', 'golf', 'board-games', 'other'];
  const makes = ['Saab', 'Mercedes', 'Dodge', 'Chevrolet', 'Audi', 'Toyota', 'Ford', 'Nissan'];
  const models = ['92x', 'E400', 'RAM', 'Tahoe', 'A5', 'Camry', 'F150', 'Pathfinder'];

  const data = [];
  
  // Generate 150 claims
  // 12 Fraudulent (approx 8.0%), 3 Under Review (approx 2.0%), 135 Genuine (approx 90.0%)
  for (let i = 0; i < 150; i++) {
    const policy_number = 100000 + i * 3721 + (i % 7) * 97;
    const age = 20 + (i % 45) + (i % 3);
    const months_as_customer = (age - 18) * 12 + (i % 12);
    
    // Status distribution
    let fraud_status = 'Genuine';
    if (i < 12) {
      fraud_status = 'Fraudulent';
    } else if (i >= 12 && i < 15) {
      fraud_status = 'Under Review';
    }

    // Severity distribution: Fraudulent claims tend to have major damage
    let severity = severities[i % 4];
    if (fraud_status === 'Fraudulent') {
      severity = i % 2 === 0 ? 'Major Damage' : 'Total Loss';
    }

    // Hobby distribution: Fraudulent claims tend to have chess/yachting/skydiving hobbies
    let hobby = hobbies[i % hobbies.length];
    if (fraud_status === 'Fraudulent') {
      hobby = i % 3 === 0 ? 'chess' : (i % 3 === 1 ? 'yachting' : 'skydiving');
    }

    // Claim amount
    let claim = 15000 + (i % 10) * 8000 + (i % 3) * 3000;
    if (severity === 'Major Damage' || severity === 'Total Loss') {
      claim += 40000 + (i % 5) * 5000;
    }
    if (severity === 'Trivial Damage') {
      claim = 1000 + (i % 5) * 800;
    }

    const state = states[i % states.length];
    const incident_type = incidentTypes[i % incidentTypes.length];
    const collision_type = severity === 'Trivial Damage' || incident_type === 'Vehicle Theft' ? 'Unknown' : collisionTypes[i % 3];
    const education = educations[i % educations.length];
    const sex = i % 2 === 0 ? 'MALE' : 'FEMALE';
    const premium = 900 + (i % 15) * 60;
    const deductible = (i % 3 === 0) ? 500 : ((i % 3 === 1) ? 1000 : 2000);
    const witnesses = i % 4;
    const injuries = i % 3;
    const hour = (8 + i * 7) % 24;
    const vehicles = (incident_type === 'Multi-vehicle Collision') ? 2 + (i % 3) : 1;
    const safety = 30 + (i % 65);
    const date = `2015-0${1 + (i % 2)}-${10 + (i % 20)}`; // Jan or Feb 2015

    data.push({
      months_as_customer,
      age,
      policy_number,
      policy_bind_date: `200${i % 9}-05-${10 + (i % 15)}`,
      policy_state: state,
      policy_csl: (i % 3 === 0) ? '250/500' : ((i % 3 === 1) ? '100/300' : '500/1000'),
      policy_deductable: deductible,
      policy_annual_premium: premium,
      umbrella_limit: i % 5 === 0 ? 3000000 : 0,
      insured_zip: 430000 + (i % 99) * 100,
      insured_sex: sex,
      insured_education_level: education,
      insured_occupation: 'professional',
      insured_hobbies: hobby,
      insured_relationship: i % 4 === 0 ? 'husband' : 'unmarried',
      'capital-gains': i % 3 === 0 ? 35000 : 0,
      'capital-loss': i % 4 === 0 ? -15000 : 0,
      incident_date: date,
      incident_type,
      collision_type,
      incident_severity: severity,
      authorities_contacted: i % 5 === 0 ? 'Police' : 'None',
      incident_state: state,
      incident_city: 'CityCenter',
      incident_location: 'Main Street',
      incident_hour_of_the_day: hour,
      number_of_vehicles_involved: vehicles,
      property_damage: i % 3 === 0 ? 'YES' : 'NO',
      bodily_injuries: injuries,
      witnesses,
      police_report_available: i % 2 === 0 ? 'YES' : 'NO',
      total_claim_amount: claim,
      injury_claim: Math.round(claim * 0.15),
      property_claim: Math.round(claim * 0.15),
      vehicle_claim: Math.round(claim * 0.7),
      auto_make: makes[i % makes.length],
      auto_model: models[i % models.length],
      auto_year: 2000 + (i % 16),
      fraud_reported: fraud_status
    });
  }
  return data;
};

const DEFAULT_CLAIMS_DATA = generateMockClaims();
