package exportxlsx

import (
	"fmt"

	"github.com/Juan-Barraza/apiGoMl/utils"
	"github.com/xuri/excelize/v2"
)

const (
	BatchSize  = 1000
	MaxWorkers = 1000
)

func ExportXLSX(dataIngress []utils.IngressRecordData) (*excelize.File, error) {
	var fieldsToXlsx = []string{"TimeStamp", "DocumentNumber", "Gender", "UserType", "Dependency", "AcademicProgram", "Reason"}
	headers := make([]string, 7)
	for i, field := range fieldsToXlsx {
		headers[i] = fieldTranslations[field]
	}

	// Crear el archivo XLSX
	file := excelize.NewFile()
	sheetName := "Datos generales"
	sheetIndex, err := file.NewSheet(sheetName)
	if err != nil {
		return nil, fmt.Errorf("error creando la hoja: %w", err)
	}
	file.DeleteSheet("Sheet1")

	// Agregar la fila de encabezado
	for i, header := range headers {
		cell := string(rune('A'+i)) + "1"
		file.SetCellValue(sheetName, cell, header)
	}

	err = ProcessDataIngressRecordConcurrent(dataIngress, file, fieldsToXlsx, sheetName)
	if err != nil {
		return nil, fmt.Errorf("error procesando clientes: %w", err)
	}

	file.SetActiveSheet(sheetIndex)
	return file, nil
}
