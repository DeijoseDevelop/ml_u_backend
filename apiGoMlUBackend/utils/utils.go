package utils

import (
	"strconv"
	"time"
)

type Filters struct {
	CounterSitePrincipal bool
	CounterSiteDowntown  bool
	CounterTotal         bool
	LoanBook             bool
	LoanComputer         bool
	ConsultRoom          bool
}

type ChartData struct {
	Service string         `json:"service"`
	Data    map[string]int `json:"data"`
}

type TotalPerSite struct {
	Site  string `json:"site"`
	Total int    `json:"total"`
}

type CombinedResponse struct {
	Services []ChartData    `json:"services"`
	Totals   []TotalPerSite `json:"totals"`
}

type IngressRecordData struct {
	TimeStamp       *time.Time `json:"time_stamp"`
	DocumentNumber  string     `json:"document_number"`
	Gender          string     `json:"gender"`
	UserType        string     `json:"user_type"`
	Reason          string     `json:"reason"`
	Dependency      string     `json:"dependency"`
	AcademicProgram string     `json:"academic_program"`
}

func ParseBoolParams(param string) (bool, error) {
	if param == "" {
		return false, nil
	}
	parseValue, err := strconv.ParseBool(param)
	if err != nil {
		return false, err
	}

	return parseValue, nil
}
