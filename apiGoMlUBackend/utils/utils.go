package utils

import "strconv"

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
