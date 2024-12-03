# Create queries
CREATE_CPA = """CREATE TABLE IF NOT EXISTS CPA
(id SERIAL PRIMARY KEY, 
firstName TEXT, 
lastName TEXT,
email TEXT,
licenseNumber TEXT,
licenseExpiration DATE);"""

CREATE_CLIENTS = """CREATE TABLE IF NOT EXISTS Clients
(id SERIAL PRIMARY KEY, 
firstName TEXT, 
lastName TEXT,
address TEXT,
city TEXT,
state TEXT,
income INTEGER,
providedMaterials boolean,
CPA_id INTEGER REFERENCES CPA(id));"""

CREATE_TAX_ASSISTANT = """CREATE TABLE IF NOT EXISTS TaxAssistant
(id SERIAL PRIMARY KEY,
firstName TEXT,
lastName TEXT)"""

CREATE_TAX_RETURN = """CREATE TABLE IF NOT EXISTS TaxReturn
(id SERIAL PRIMARY KEY,
timestamp INTEGER,
fileStatus boolean,
CPA_check boolean,
Client_id INTEGER REFERENCES Clients(id),
Assistant_id INTEGER REFERENCES TaxAssistant(id),
CPA_id INTEGER REFERENCES CPA(id));"""

# Insert queries
INSERT_CLIENT_RETURN_ID = """INSERT INTO Clients (firstName, lastName, address, city, state, income, providedMaterials, CPA_id)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id;"""

INSERT_CPA_RETURN_ID = """INSERT INTO CPA (firstName, lastName, email, licenseNumber, licenseExpiration) 
VALUES (%s,%s,%s,%s,%s) RETURNING id;"""

INSERT_TAX_RETURN = """INSERT INTO TaxReturn (timestamp, fileStatus, CPA_check, Client_id, Assistant_id, CPA_id)
 VALUES (%s, %s, %s, %s, %s, %s);"""

INSERT_TAX_ASSISTANT = """INSERT INTO TaxAssistant (firstName, lastName) VALUES (%s,%s) RETURNING id;"""

# Select queries
SELECT_RANDOM_CPA = """SELECT id FROM CPA ORDER BY RANDOM() LIMIT 1;"""

SELECT_CLIENT = """SELECT * FROM Clients WHERE id = %s;"""

SELECT_ASSISTANT = """SELECT * FROM TaxAssistant WHERE id = %s;"""

SELECT_CPA = """SELECT * FROM CPA WHERE id = %s;"""

SELECT_ALL_TAX_RETURNS = """SELECT TaxReturn.*, Clients.firstName, Clients.lastName
FROM TaxReturn
JOIN Clients
ON TaxReturn.Client_id = Clients.id;"""

# Check for client Tax Returns
SELECT_CLIENT_RETURN = """SELECT 
    Clients.id AS client_id, 
    Clients.firstName AS client_first_name, 
    Clients.lastName AS client_last_name, 
    TaxReturn.timestamp, 
    TaxReturn.fileStatus, 
    TaxReturn.CPA_check, 
    CPA.id AS cpa_id, 
    CPA.firstName AS cpa_first_name, 
    CPA.lastName AS cpa_last_name
FROM Clients
LEFT JOIN TaxReturn
ON Clients.id = TaxReturn.Client_id
LEFT JOIN CPA
ON TaxReturn.CPA_id = CPA.id
WHERE Clients.id = %s;"""


# Update client status
UPDATE_MATERIALS_STATUS = """UPDATE Clients SET providedMaterials = %s WHERE id = %s;"""

UPDATE_RETURN_STATUS_CPA = """UPDATE TaxReturn
SET timestamp = %s, fileStatus = %s, CPA_check = %s, CPA_id = %s
WHERE id = %s;"""

UPDATE_RETURN_STATUS_ASSISTANT = """UPDATE TaxReturn
SET timestamp = %s, fileStatus = %s, CPA_check = %s, Assistant_id = %s
WHERE id = %s;"""
