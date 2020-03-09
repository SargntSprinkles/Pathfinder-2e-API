package ancestries

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/gocolly/colly"
	"github.com/gorilla/mux"
)

var all []Ancestry

// var expireTimer = 30 * time.Minute
var expireTimer = 10 * time.Second

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

// GetAll : returns an array of all ancestries
func GetAll() []Ancestry {
	scrapeAll()
	return all
}

// List : encodes all ancestries into json
func List(w http.ResponseWriter, r *http.Request) {
	pretty, err := json.MarshalIndent(GetAll(), "", "    ")
	if err != nil {
		fmt.Fprintf(w, "List()/json.MarshalIndent - We need to learn how to handle errors better: %s", err)
	}
	fmt.Fprint(w, string(pretty))
}

// GetByName : attempts to find the provided ancestry
func GetByName(name string) (Ancestry, bool) {
	for _, a := range all {
		if strings.ToLower(a.Name) == strings.ToLower(name) {
			a.scrape()
			return a, true
		}
	}
	return Ancestry{}, false
}

// Get : encodes the requested ancestry into json or reports an error
func Get(w http.ResponseWriter, r *http.Request) {
	if len(all) == 0 {
		scrapeAll()
	}

	name := mux.Vars(r)["name"]
	ancestry, found := GetByName(name)
	if !found {
		fmt.Fprintf(w, "Ancestry \"%s\" not found! This should be a 404 message", name)
	} else {
		pretty, err := json.MarshalIndent(ancestry, "", "    ")
		if err != nil {
			fmt.Fprintf(w, "Get()/json.MarshalIndent - We need to learn how to handle errors better: %s", err)
		}
		fmt.Fprint(w, string(pretty))
		// json.NewEncoder(w).Encode(ancestry)
	}
}

// Equals : checks if another Ancestry is the same as this one
func (a *Ancestry) Equals(a2 Ancestry) bool {
	if a.Name == a2.Name {
		return true
	}
	return false
}

func scrapeAll() {
	// http://2e.aonprd.com/Ancestries.aspx
	// Name: <h2 class="title">
	collector := colly.NewCollector(colly.AllowedDomains("2e.aonprd.com"))
	collector.OnHTML("h2", func(ancestryHeader *colly.HTMLElement) {
		if ancestryHeader.Attr("class") == "title" {
			relativeURL := ""
			ancestryHeader.ForEach("a", func(_ int, ancestryLink *colly.HTMLElement) {
				relativeURL = ancestryLink.Attr("href")
			})
			tmpAncestry := Ancestry{
				Name: ancestryHeader.Text,
				URL:  "http://2e.aonprd.com/" + relativeURL,
			}

			_, found := GetByName(tmpAncestry.Name)

			//if the ancestry doesn't exist in "all", scrape it and add it to "all"
			if !found {
				tmpAncestry.scrape()
				all = append(all, tmpAncestry)
			}
		}
	})
	collector.Visit("http://2e.aonprd.com/Ancestries.aspx")
}

func (a *Ancestry) scrape() {
	if a.URL != "" && (time.Now().After(a.LastUpdated.Add(expireTimer)) ||
		len(a.Traits) == 0 ||
		len(a.Boosts) == 0 ||
		len(a.Flaws) == 0 ||
		len(a.Languages) == 0 ||
		a.Size == "") {
		collector := colly.NewCollector(colly.AllowedDomains("2e.aonprd.com"))
		// Traits: <span class="trait">
		a.Traits = []string{}
		collector.OnHTML("span", func(trait *colly.HTMLElement) {
			if trait.Attr("class") == "trait" {
				a.Traits = append(a.Traits, trait.Text)
			}
		})
		collector.OnHTML("span", func(descriptionGeneral *colly.HTMLElement) {
			if descriptionGeneral.Attr("id") == "ctl00_MainContent_DetailedOutput" {
				a.Description.General = descriptionGeneral.Text
			}
		})
		collector.Visit(a.URL)
		a.LastUpdated = time.Now()
	}
}
