package services

import "github.com/Juan-Barraza/apiGoMl/repositories"

type DataService struct {
	Repo *repositories.DataRepositoty
}

func NewDataService(repo *repositories.DataRepositoty) *DataService {
	return &DataService{Repo: repo}
}

func (s *DataService) GetUsers() ([]map[string]interface{}, error) {
	return s.Repo.GetUser()
}
