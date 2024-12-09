package services

import (
	"fmt"

	"github.com/Juan-Barraza/apiGoMl/repositories"
	"github.com/Juan-Barraza/apiGoMl/utils"
)

type DataService struct {
	Repo *repositories.DataRepositoty
}

func NewDataService(repo *repositories.DataRepositoty) *DataService {
	return &DataService{Repo: repo}
}

func (s *DataService) GetUsers() ([]map[string]interface{}, error) {
	return s.Repo.GetUser()
}

func (s *DataService) GetInformation(filters utils.Filters) (int, error) {
	result, err := s.Repo.GetInformationRecord(filters)
	if err != nil {
		return 0, err
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
