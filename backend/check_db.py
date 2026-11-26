import sqlite3
conn = sqlite3.connect(r'C:\TechMahindra\Day1\ai-suitability-advisor\backend\ai_suitability_advisor.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print('Tables:', tables)
cursor.close()
conn.close()