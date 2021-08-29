<script>
    import { covid } from "../stores/covidStore";
    import NewCases from "../templates/NewCases.svelte";
    import DataTable from "../components/DataTable.svelte";
</script>

<svelte:head>
    <title>Analysis</title>
</svelte:head>

<main>
    <h1 style="text-align: center; font-size: 50px;">COVID-19 Analysis in Bosnia and Herzegovina</h1>
    <article id="table-1">
        <DataTable />
    </article>
    <caption><strong>Table - 1</strong>: The table gives you a look at the data that is going to be analyzed in this report.</caption>
    
    <article id="project-intro">
        <h1 class="header-h1-content">The data geathering methods and the algorithm structure</h1>
            <p>
                To gather the data we needed to first find the sources for the data and it was not easy. The first problem we faced is that there was no data source to be found,
                the agencies and the government did not care about the COVID-19 data gathering.
            </p>
            <p>
                And the first month of the COVID-19 crisis we had no data from the local government, so we turned to inernational resources and found <a href="https://ourworldindata.org/coronavirus">
                Our World in Data</a> And from there we gather our new cases and total casses, because it is the most reliable source.
            </p>
            <p>
                Then as the pandemic took off the local government started to display some data on their <a href="http://www.mcp.gov.ba/Publication/Category/projekti?category=7">website</a>
                But the data was inconsistent, the table structure often changed and there was missing data. Those are critical problems because a government authority must provide transparent, clean and 
                understandable data to justify their work to the citizens.
            </p>
            <p>
                Facing all of these problems we needed to find a solution, and we did. The new cases and the total cases we gathered from the OurWorldinData, and the data about the 
                number of recovered, tested and died people we got from the government's website. The data gathered from the government website needed to be parsed through multiple
                custom algorithms to be usable.
            </p>

            <h2 class="header-h2-content">Data collection and processing steps</h2>
            <h3 class="header-h3-content">Step one:</h3>
            <p>
                The data set we collected from <a href="https://ourworldindata.org/coronavirus">Our World in Data</a> was shipped in excel and it was easy with <a href="https://www.python.org/">Python</a> to read the data and extract the information we needed. The government source
                was far more difficult, because the data didn't shipp in any kind of a data structure we needed to find some way to extract the data. We then decided to scrape the data with
                <a href="https://www.crummy.com/software/BeautifulSoup/">Beautiful Soup</a>.
            </p> 
            <h3 class="header-h3-content">Step two:</h3>
            <p>
               In this step we needed to somehow parse the data, with the excel file it was easy, load it to <a href="https://pandas.pydata.org/">Pandas</a> and we are good to go, but with the government data, we
               had a problem, the scraped data had inconsistenties with the data, table structure and as a "bonus" it shipped in plain HTML. 
            </p> 
            <p>
                We first needed to get rid off the HTML tags, once that was done we turned our attention to the table structure inconsistenties and identified the dates where the table
                structure was changing. Now the algorithm know's where to group the data regardless is the column there or not. 
            </p>
            <p>
                Then there was the problem with the missing data. We addressed this problem per column because the number of tested people can't be filled the same way that the died people
                column get's filled. So the columns (New Cases, Recovered, Tested) are filled with the mean of the last 5 days and the died column with the last 3 days.
            </p>
            <h3 class="header-h3-content">Step three:</h3>
            <p>
                As the data was cleaned we exported it to excel and json. So everyone who want's the data can get it over the API or in the excel file. And we ended up with the result
                shown in the <a href="#table-1">Table - 1</a>.
            </p>
    </article>

    <article id="covid-new-cases">
        <h1>Analysing the data</h1>
       
        <figure id="chart-1">
            <NewCases />
            <figcaption><strong>Chart - 1</strong>: Number of New Cases of COVID-19 virus in Bosnia and Herzegovina from April 2020. until Today</figcaption>
        </figure>

        
        <p style="margin-top: 20px;">
            <a href="#chart-1">Chart - 1</a> shows us how much people were infected with the virus through the year. To understand more about the
            curve and the pandemic we need to break it down into multiple subcharts where we can better see the situation and anlyse the situation.
        </p>
        <!-- 28.06.2020 -->

    </article>
</main>





<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300&display=swap');

    main{
        margin-top: 150px;

        display: grid;
        grid-template-columns: 80%;
        grid-row-gap: 30px;

        justify-content: center;
    }
    :global(body){
        font-family: 'Poppins', sans-serif;
    }

    :global(h1){
        margin-top: 30px;
        text-align: left;
        font-size: 30px;
        font-weight: bold;
    }
    :global(h2){
        margin-top: 30px;
        text-align: left;
        font-size: 28px;
        font-weight: bold;
    }
    :global(h3){
        margin-top: 30px;
        text-align: left;
        font-size: 26px;
        font-weight: bold;
    }
    :global(p){
        font-size: 18px;
    }
    :global(a){
        text-decoration: none;
    }
    :global(.tick line) {
        stroke: #c0c0bb;
    }
    
    :global(.tick text){
        font-size: 14px;
        fill: #635f5d;
    }

</style>