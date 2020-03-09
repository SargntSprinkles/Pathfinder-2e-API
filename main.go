package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/SargntSprinkles/Pathfinder-2e-API/pathfinder/ancestries"
	"github.com/gorilla/mux"
)

func main() {
	router := mux.NewRouter().StrictSlash(true)
	router.HandleFunc("/", rootHandler)
	// router.HandleFunc("/actions/", actions.List)
	// router.HandleFunc("/actions/{name}", actions.Get)
	router.HandleFunc("/ancestries/", ancestries.List)
	router.HandleFunc("/ancestries/{name}", ancestries.Get)
	// router.HandleFunc("/archetypes/", archetypes.List)
	// router.HandleFunc("/archetypes/{name}", archetypes.Get)
	// router.HandleFunc("/backgrounds/", backgrounds.List)
	// router.HandleFunc("/backgrounds/{name}", backgrounds.Get)
	// router.HandleFunc("/classes/", classes.List)
	// router.HandleFunc("/classes/{name}", classes.Get)
	// router.HandleFunc("/conditions/", conditions.List)
	// router.HandleFunc("/conditions/{name}", conditions.Get)
	// router.HandleFunc("/equipment/", equipment.List)
	// router.HandleFunc("/equipment/{name}", equipment.Get)
	// router.HandleFunc("/feats/", feats.List)
	// router.HandleFunc("/feats/{name}", feats.Get)
	// router.HandleFunc("/hazards/", hazards.List)
	// router.HandleFunc("/hazards/{name}", hazards.Get)
	// router.HandleFunc("/monsters/", monsters.List)
	// router.HandleFunc("/monsters/{name}", monsters.Get)
	// router.HandleFunc("/skills/", skills.List)
	// router.HandleFunc("/skills/{name}", skills.Get)
	// router.HandleFunc("/spells/", spells.List)
	// router.HandleFunc("/spells/{name}", spells.Get)
	log.Fatal(http.ListenAndServe(":8080", router))
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the Pathfinder 2e API!\nAll data comes directly from Archives of Nethys\n%s", r.URL.Path[1:])
}
