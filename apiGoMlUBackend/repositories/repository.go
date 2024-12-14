package repositories

import (
	"database/sql"
	"fmt"
	"strings"

	"github.com/Juan-Barraza/apiGoMl/utils"
)

type DataRepository struct {
	DB *sql.DB
}

func NewDataRepository(db *sql.DB) *DataRepository {
	return &DataRepository{DB: db}
}

func (r *DataRepository) GetFilteredDashboardData(filters utils.Filters) (*utils.CombinedResponse, error) {
	whereClause, params := r.buildWhereClause(filters)

	// Consulta principal para los datos del gráfico
	query := fmt.Sprintf(`
        SELECT 
            ir.reason AS service, 
            LOWER(ir.site) AS site, 
            LOWER(u.dependency) AS dependency, 
            COUNT(*) AS total
        FROM 
            ingress_records ir
        JOIN
            users u ON ir.user_id = u.id
        %s
        GROUP BY ir.reason, ir.site, u.dependency
        ORDER BY ir.reason, ir.site, u.dependency;
    `, whereClause)

	rows, err := r.DB.Query(query, params...)
	if err != nil {
		return nil, fmt.Errorf("error al ejecutar la consulta principal: %w", err)
	}
	defer rows.Close()

	chartData, err := r.formatChartData(rows)
	if err != nil {
		return nil, fmt.Errorf("error al formatear datos del gráfico: %w", err)
	}

	// Consulta para los totales por sede
	totalsQuery := fmt.Sprintf(`
        SELECT 
            site, 
            COUNT(*) AS total
        FROM 
            ingress_records ir
        JOIN
            users u ON ir.user_id = u.id
        %s
        GROUP BY site
        ORDER BY site;
    `, whereClause)

	totalRows, err := r.DB.Query(totalsQuery, params...)
	if err != nil {
		return nil, fmt.Errorf("error al ejecutar la consulta de totales: %w", err)
	}
	defer totalRows.Close()

	combinedTotals := make(map[string]int)

	var totals []utils.TotalPerSite
	for totalRows.Next() {
		var site string
		var total int

		if err := totalRows.Scan(&site, &total); err != nil {
			return nil, fmt.Errorf("error al escanear totales: %w", err)
		}

		site = strings.ToLower(site)
		if existingTotal, exist := combinedTotals[site]; exist {
			combinedTotals[site] = existingTotal + total
		} else {
			combinedTotals[site] = total
		}
	}

	for site, total := range combinedTotals {
		totals = append(totals, utils.TotalPerSite{
			Site:  site,
			Total: total,
		})
	}

	return &utils.CombinedResponse{
		Services: chartData,
		Totals:   totals,
	}, nil
}

func (r *DataRepository) buildWhereClause(filters utils.Filters) (string, []interface{}) {
	var whereClauses []string
	var params []interface{}

	if filters.Site != "" {
		whereClauses = append(whereClauses, "LOWER(ir.site) = ?")
		params = append(params, strings.ToLower(filters.Site))
	}

	if filters.StartDate != nil {
		whereClauses = append(whereClauses, "ir.time_stamp >= ?")
		params = append(params, filters.StartDate)
	}

	if filters.EndDate != nil {
		whereClauses = append(whereClauses, "ir.time_stamp <= ?")
		params = append(params, filters.EndDate)
	}

	if filters.AcademicProgram != "" {
		whereClauses = append(whereClauses, "u.academic_program = ?")
		params = append(params, filters.AcademicProgram)
	}

	if filters.DocumentNumber != "" {
		whereClauses = append(whereClauses, "u.document_number = ?")
		params = append(params, filters.DocumentNumber)
	}

	if filters.Dependency != "" {
		whereClauses = append(whereClauses, "LOWER(u.dependency) = ?")
		params = append(params, strings.ToLower(filters.Dependency))
	}

	if filters.Reason != "" {
		whereClauses = append(whereClauses, "LOWER(ir.reason) = ?")
		params = append(params, strings.ToLower(filters.Reason))
	}

	whereClause := ""
	if len(whereClauses) > 0 {
		whereClause = "WHERE " + strings.Join(whereClauses, " AND ")
	}

	return whereClause, params
}

func (r *DataRepository) formatChartData(rows *sql.Rows) ([]utils.ChartData, error) {
	groupedData := map[string]map[string]map[string]int{}

	for rows.Next() {
		var service, site, dependency string
		var total int

		if err := rows.Scan(&service, &site, &dependency, &total); err != nil {
			return nil, fmt.Errorf("error al escanear filas: %w", err)
		}

		if _, exists := groupedData[service]; !exists {
			groupedData[service] = map[string]map[string]int{}
		}
		if _, exists := groupedData[service][site]; !exists {
			groupedData[service][site] = map[string]int{}
		}

		// Si 'dependency' está vacío, se agrupan bajo "all"
		if dependency != "" {
			groupedData[service][site][dependency] = total
		} else {
			if _, exists := groupedData[service][site]["all"]; !exists {
				groupedData[service][site]["all"] = 0
			}
			groupedData[service][site]["all"] += total
		}
	}

	var chartData []utils.ChartData
	for service, siteData := range groupedData {
		siteDependencyData := map[string]int{}
		for site, dependencies := range siteData {
			for dependency, count := range dependencies {
				siteDependencyData[fmt.Sprintf("%s (%s)", site, dependency)] = count
			}
		}
		chartData = append(chartData, utils.ChartData{
			Service: service,
			Data:    siteDependencyData,
		})
	}

	return chartData, nil
}

func (r *DataRepository) GetChartData() ([]utils.ChartData, error) {
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

func (r *DataRepository) GetTotalPerSite() ([]utils.TotalPerSite, error) {
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

func (r *DataRepository) GetDataForFileXlsx() ([]utils.IngressRecordData, error) {
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
