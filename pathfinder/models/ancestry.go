package models

import (
	"time"
)

// Ancestry : a.k.a. race
type Ancestry struct {
	Name        string              `json:"Name"`
	Traits      []string            `json:"Traits"`
	Description AncestryDescription `json:"Description"`
	HP          int                 `json:"HP"`
	Size        string              `json:"Size"`
	Speed       int                 `json:"Speed"`
	Boosts      []string            `json:"Boosts"`
	Flaws       []string            `json:"Flaws"`
	Languages   []string            `json:"Languages"`
	Specials    []AncestrySpecial   `json:"Specials"`
	URL         string              `json:"URL"`
	LastUpdated time.Time           `json:"LastUpdated"`
}

// AncestryDescription : description of the ancestry
type AncestryDescription struct {
	General             string   `json:"General"`
	YouMight            []string `json:"YouMight"`
	OthersProbably      []string `json:"OthersProbably"`
	PhysicalDescription string   `json:"PhysicalDescription"`
	Society             string   `json:"Society"`
	AlignmentReligion   string   `json:"AlignmentReligion"`
	Names               string   `json:"Names"`
	SampleNames         []string `json:"SampleNames"`
}

// AncestrySpecial : the special abilities of an ancestry
type AncestrySpecial struct {
	Name        string
	Description string
}
