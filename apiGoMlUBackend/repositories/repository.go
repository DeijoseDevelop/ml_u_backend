package repositories

import (
	"database/sql"
	"log"
)

type DataRepositoty struct {
	DB *sql.DB
}

func NewDataRepository(db *sql.DB) *DataRepositoty {
	return &DataRepositoty{DB: db}
}

func (r *DataRepositoty) GetUser() ([]map[string]interface{}, error) {
	query := "SELECT id, name FROM users"
	rows, err := r.DB.Query(query)
	if err != nil {
		log.Println("Error ejecutando la consulta:", err)
		return nil, err
	}
	defer rows.Close()
	var results []map[string]interface{}

	for rows.Next() {
		var id int
		var name string
		if err := rows.Scan(&id, &name); err != nil {
			log.Println("Error escaneando los datos:", err)
			return nil, err
		}
		results = append(results, map[string]interface{}{
			"id":   id,
			"name": name,
		})
	}
	return results, nil
}
