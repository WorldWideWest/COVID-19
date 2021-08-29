import { writable } from "svelte/store";


export const covid = writable([]);

const fetchCovid = async() => {
    const url = "http://127.0.0.1:8000/api/";
    const response = await fetch(url);
    const data = await response.json();
    const loadData = data.map(d => {


        
        return {
            "date": d.date,
            "total_cases": +d.total_cases,
            "new_cases": +d.new_cases,
            "recovered": +d.recovered,
            "tested": +d.tested,
            "died": +d.died
        }
    });

    covid.set(loadData);

}

fetchCovid();