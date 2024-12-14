package services

import (
	"fmt"

	"github.com/Juan-Barraza/apiGoMl/repositories"
	export "github.com/Juan-Barraza/apiGoMl/services/exportXlsx"
	"github.com/Juan-Barraza/apiGoMl/utils"
	"github.com/xuri/excelize/v2"
)

type DataService struct {
	Repo *repositories.DataRepository
}

func NewDataService(repo *repositories.DataRepository) *DataService {
	return &DataService{Repo: repo}
}

func (s *DataService) GetInformation(filters utils.Filters) (*utils.CombinedResponse, error) {
	result, err := s.Repo.GetFilteredDashboardData(filters)
	if err != nil {
		return nil, fmt.Errorf("error en el servicio al obtener información: %w", err)
	}
	return result, nil
}

func (s *DataService) GetCombinedData() (*utils.CombinedResponse, error) {
	servicesData, err := s.Repo.GetChartData()
	if err != nil {
		return nil, fmt.Errorf("error al obtener datos de servicio")
	}
	totalsData, err := s.Repo.GetTotalPerSite()
	if err != nil {
		return nil, fmt.Errorf("error al obtener total de datos")
	}

	combinationResponse := &utils.CombinedResponse{
		Services: servicesData,
		Totals:   totalsData,
	}

	return combinationResponse, nil

}

func (s *DataService) ExportDataIngressRecord() (*excelize.File, error) {
	dataIngressRecord, err := s.Repo.GetDataForFileXlsx()
	if err != nil {
		return nil, err
	}

	if len(dataIngressRecord) == 0 {
		return nil, nil
	}

	file, err := export.ExportXLSX(dataIngressRecord)
	if err != nil {
		return nil, fmt.Errorf("error al crear archivo")
	}

	return file, nil
}
