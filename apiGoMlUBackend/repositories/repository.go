package repositories

import (
	"database/sql"
	"fmt"
	"log"
	"strings"

	"github.com/Juan-Barraza/apiGoMl/utils"
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

func (r *DataRepositoty) GetInformationRecord(filters utils.Filters) (int, error) {
	var results int
	query := "SELECT COUNT(*) FROM ingress_records WHERE 1=1"
	var conditions []string

	if filters.CounterSitePrincipal {
		conditions = append(conditions, "site = 'Sede cuatro vientos'")
	}

	if filters.CounterSiteDowntown {
		conditions = append(conditions, "site = 'Sede centro'")
	}

	if filters.LoanBook {
		conditions = append(conditions, "reason = 'Prestamo de libros'")
	}

	if filters.LoanComputer {
		conditions = append(conditions, "reason = 'Prestamo de computadoras'")
	}

	if filters.ConsultRoom {
		conditions = append(conditions, "reason = 'Consulta en sala'")
	}

	if filters.CounterTotal {
		query = "SELECT COUNT(*) FROM ingress_records"
	} else if len(conditions) > 0 {
		// Si hay condiciones, agregarlas a la consulta
		query += " AND " + strings.Join(conditions, " AND ")
	}

	// Ejecutar la consulta
	rows, err := r.DB.Query(query)
	if err != nil {
		log.Fatal("Error ejecutando la consulta:", err)
		return 0, err
	}
	defer rows.Close()

	if rows.Next() {
		err := rows.Scan(&results)
		if err != nil {
			return 0, fmt.Errorf("error escaneando el resultado: %v", err)
		}
	} else {
		return 0, fmt.Errorf("no se encontraron resultados")
	}

	return results, nil
}

func (r *DataRepositoty) GetChartData() ([]utils.ChartData, error) {
	query := `
		SELECT 
			reason AS service,
			site,
			COUNT(*) AS total
		FROM 
			ingress_records
		GROUP BY 
			reason, site
		ORDER BY 
			reason, site;
	`

	rows, err := r.DB.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	groupedData := map[string]map[string]int{}

	for rows.Next() {
		var service, site string
		var total int

		if err := rows.Scan(&service, &site, &total); err != nil {
			return nil, err
		}

		if _, exists := groupedData[service]; !exists {
			groupedData[service] = make(map[string]int)
		}
		groupedData[service][site] = total
	}

	var chartData []utils.ChartData
	for service, siteData := range groupedData {
		chartData = append(chartData, utils.ChartData{
			Service: service,
			Data:    siteData,
		})
	}

	return chartData, nil
}

func (r *DataRepositoty) GetTotalPerSite() ([]utils.TotalPerSite, error) {
	query := `
		SELECT 
    		site,
    		COUNT(*) AS total
		FROM 
    		ingress_records
		GROUP BY 
    		site
		ORDER BY 
    		site;

	`

	rows, err := r.DB.Query(query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []utils.TotalPerSite

	for rows.Next() {
		var result utils.TotalPerSite

		if err := rows.Scan(&result.Site, &result.Total); err != nil {
			return nil, err
		}

		results = append(results, result)
	}

	return results, nil
}

func (r *DataRepositoty) GetDataForFileXlsx() ([]utils.IngressRecordData, error) {
	query := `
		SELECT 
			ingress_records.time_stamp, 
			ingress_records.reason,
			users.document_number, 
			users.user_type, 
			users.dependency, 
			users.academic_program, 
			users.gender
		FROM 
			ingress_records
		JOIN 
			users ON users.id = ingress_records.user_id
`

	// Ejecuta la consulta
	rows, err := r.DB.Query(query)
	if err != nil {
		return nil, fmt.Errorf("error al ejecutar la consulta: %v", err)
	}
	defer rows.Close()

	if rows == nil {
		return nil, fmt.Errorf("no se obtuvieron filas")
	}

	// Procesa los resultados
	var records []utils.IngressRecordData
	for rows.Next() {
		var record utils.IngressRecordData
		err := rows.Scan(
			&record.TimeStamp,
			&record.Reason,
			&record.DocumentNumber,
			&record.UserType,
			&record.Dependency,
			&record.AcademicProgram,
			&record.Gender,
		)
		if err != nil {
			return nil, fmt.Errorf("error al escanear los datos: %v", err)
		}
		records = append(records, record)
	}

	if err = rows.Err(); err != nil {
		return nil, fmt.Errorf("error durante la iteración de filas: %v", err)
	}

	return records, nil
}
