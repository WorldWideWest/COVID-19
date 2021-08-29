<script>
    import { covid } from "../stores/covidStore";
    import moment from "moment";

    let data = [];
    $:{
        data = [...$covid];
    }

</script>

<div class="fixTableHead table-responsive">
    <table class="table table-hover table-fluid" id="covid-table">
        <thead>
            <tr>
                <th>Date</th>
                <th>Total Cases</th>
                <th>New Cases</th>
                <th>Recovered</th>
                <th>Tested</th>
                <th>Died</th>
            </tr>
        </thead>
        <tbody>
            {#each data as cv }
                <tr>
                    <td>{ cv.date }</td>
                    <td>{ cv.total_cases }</td>
                    <td>{ cv.new_cases}</td>
                    <td>{ cv.recovered }</td>
                    <td>{ cv.tested }</td>
                    <td>{ cv.died }</td>
                </tr>
            {/each}
        </tbody>
    </table>
</div>


<style>
    .fixTableHead {
      overflow-y: auto;
      height: 300px;
    }
    .fixTableHead thead th {
      position: sticky;
      top: 0;
    }
    table {
      border-collapse: collapse;        
      width: 100%;
      text-align: center;
    }
    th,
    td {
      padding: 8px 15px;
    }
    th {
      background: #d3d3d4;
    }

    ::-webkit-scrollbar {
        width: 12px;
    }

    /* Track */
    ::-webkit-scrollbar-track {
        background: #fff;
    }

    /* Handle */
    ::-webkit-scrollbar-thumb {
        background: #888;
        border-radius: 10px;
        height: 80px;
    }

    /* Handle on hover */
    ::-webkit-scrollbar-thumb:hover {
        background: #555;
    }
    
</style>