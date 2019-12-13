package ancestries

import (
	"errors"
	"github.com/SargntSprinkles/Pathfinder-2e-API/pathfinder/models"
	"github.com/SargntSprinkles/Pathfinder-2e-API/pathfinder/scraper"
	"strings"
	"time"
)

var all []models.Ancestry = populateAll()

// populateAll : populates the list of all ancestries
func populateAll() (all []models.Ancestry) {
	testDwarf := models.Ancestry{
		Name: "Dwarf",
		Description: models.AncestryDescription{
			General: "As unpredictable",
			YouMight: []string{
				"Strive",
			},
			OthersProbably: []string{
				"Respect",
			},
			PhysicalDescription: "Humans",
			Society:             "Human",
			AlignmentReligion:   "Humanity",
			Names:               "Unlike",
			SampleNames: []string{
				"A variety",
			},
		},
		HP:    10,
		Size:  "Medium",
		Speed: 20,
		Boosts: []string{
			"Constitution",
			"Wisdom",
			"Free",
		},
		Flaws: []string{"Charisma"},
		Languages: []string{
			"Common",
			"Dwarven",
			"Additional languages equal to your Intelligence modifier (if it’s positive). Choose from Gnomish, Goblin, Jotun, Orcish, Terran, Undercommon, and any other languages to which you have access (such as the languages prevalent in your region).",
		},
		Specials: []models.AncestrySpecial{
			{Name: "Darkvision", Description: "You can see in darkness and dim light just as well as you can see in bright light, though your vision in darkness is in black and white."},
			{Name: "Clan Dagger", Description: "You get one clan dagger of your clan for free, as it was given to you at birth. Selling this dagger is a terrible taboo and earns you the disdain of other dwarves."},
		},
		URL:         "http://2e.aonprd.com/Ancestries.aspx?ID=1",
		LastUpdated: time.Now(),
	}

	testHuman := models.Ancestry{
		Name: "Human",
		Traits: []string{
			"Human",
			"Humanoid",
		},
		Description: models.AncestryDescription{
			General: "As unpredictable",
			YouMight: []string{
				"Strive",
			},
			OthersProbably: []string{
				"Respect",
			},
			PhysicalDescription: "Humans",
			Society:             "Human",
			AlignmentReligion:   "Humanity",
			Names:               "Unlike",
			SampleNames: []string{
				"A variety",
			},
		},
		HP:    8,
		Size:  "Medium",
		Speed: 25,
		Boosts: []string{
			"Free",
			"Free",
		},
		Flaws: []string{},
		Languages: []string{
			"Common",
			"Additional languages equal to 1 + your Intelligence modifier (if it’s positive). Choose from the list of common languages and any other languages to which you have access (such as the languages prevalent in your region).",
		},
		Specials:    []models.AncestrySpecial{},
		URL:         "http://2e.aonprd.com/Ancestries.aspx?ID=6",
		LastUpdated: time.Now(),
	}

	all = append(all, testDwarf, testHuman)
	return all
}

func update(a *models.Ancestry) {
	if time.Now().After(a.LastUpdated.AddDate(0, 0, 1)) {
		scraper.GetAncestry(a)
	}
}

// GetAll : returns the list of all ancestries
func GetAll() (allOfThem []models.Ancestry) {
	return all
}

// GetByName : attempts to find the provided ancestry
func GetByName(name string) (ancestry models.Ancestry, err error) {
	for _, a := range all {
		if strings.ToLower(a.Name) == strings.ToLower(name) {
			return a, nil
		}
	}
	err = errors.New("ancestry not found")
	return ancestry, err
}
