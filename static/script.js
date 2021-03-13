// /**
//  * Sorts a HTML table.
//  *
//  * @param {HTMLTableElement} table The table to sort
//  * @param {number} column The index of the column to sort
//  * @param {boolean} asc Determines if the sorting will be in ascending
//  */
// function sortTableByColumn(table, column, asc = true) {
//     const dirModifier = asc ? 1 : -1;
//     const tBody = table.tBodies[0];
//     const rows = Array.from(tBody.querySelectorAll("tr"));
//
//     // Sort each row
//     const sortedRows = rows.sort((a, b) => {
//         const aColText = a.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
//         const bColText = b.querySelector(`td:nth-child(${ column + 1 })`).textContent.trim();
//
//         return aColText > bColText ? (dirModifier) : (-1 * dirModifier);
//     });
//
//     // Remove all existing TRs from the table
//     while (tBody.firstChild) {
//         tBody.removeChild(tBody.firstChild);
//     }
//
//     // Re-add the newly sorted rows
//     tBody.append(...sortedRows);
//
//     // Remember how the column is currently sorted
//     table.querySelectorAll("th").forEach(th => th.classList.remove("th-sort-asc", "th-sort-desc"));
//     table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-asc", asc);
//     table.querySelector(`th:nth-child(${ column + 1})`).classList.toggle("th-sort-desc", !asc);
// }
//
// document.querySelectorAll(".table-sortable th").forEach(headerCell => {
//     headerCell.addEventListener("click", () => {
//         const tableElement = headerCell.parentElement.parentElement.parentElement;
//         const headerIndex = Array.prototype.indexOf.call(headerCell.parentElement.children, headerCell);
//         const currentIsAscending = headerCell.classList.contains("th-sort-asc");
//
//         sortTableByColumn(tableElement, headerIndex, !currentIsAscending);
//     });
// });

$(document).ready( function () {
	 $('#sortTable').dataTable( {
        "aoColumns": [
            null,
            null,
            null,
            null,
            { "sType": "date-uk" },
            null


        ]
    });

} );

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
"date-uk-pre": function ( a ) {
    var ukDatea = a.split('/');
    return (ukDatea[2] + ukDatea[1] + ukDatea[0]) * 1;
},

"date-uk-asc": function ( a, b ) {
    return ((a < b) ? -1 : ((a > b) ? 1 : 0));
},

"date-uk-desc": function ( a, b ) {
    return ((a < b) ? 1 : ((a > b) ? -1 : 0));
}
} );
