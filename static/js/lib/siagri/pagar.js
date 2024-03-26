var data_pagar = JSON.parse(document.getElementById('resultados_pagar').textContent);
var data_receber = JSON.parse(document.getElementById('resultados_receber').textContent);

var categorias_pagar = Object.keys(data_pagar);
var valores_pagar = Object.values(data_pagar);
var categorias_receber = Object.keys(data_receber);
var valores_receber = Object.values(data_receber);

var options_pagar = {
    series: [{
        name: 'Total a pagar',
        data: valores_pagar
    }],
    chart: {
        type: 'bar',
        height: 350,
        toolbar: {
            show: false
        },
        background: '#FFFFFF'
    },
    plotOptions: {
        bar: {
            horizontal: true,
            borderRadius: 3,
            columnWidth: '80%', // Largura das barras aumentada para 80%
            endingShape: 'rounded' // Mudança para pontas arredondadas
        }
    },
    dataLabels: {
        enabled: false,
        offsetX: -6,

    },

    title:{
        text: 'Contas a Pagar',
        align: 'center',
        offsetY: 7,
        floating: true,
        style: {
          fontSize: '13px',
          color: '#082f4f'
        }
    },
    xaxis: {
        categories: categorias_pagar,
        labels: {
            style: {
                fontSize: '12px',
                fontFamily: 'Helvetica, Arial, sans-serif'
            },
            formatter: function(val){
                return  Math.round(val / 1000).toLocaleString('pt-BR', { minimumFractionDigits: 0 }) + ' K';
            }
        }
    },
    grid: {
        show: false // Remover as linhas horizontais
    },
    tooltip: {
        enabled: true,
        shared: false,
        title: {
            text: 'Valor'
        },
        y: {
            
            formatter: function(value) {
                if (value >= 1000) {
                    return 'R$ ' + Math.round(value / 1000).toLocaleString('pt-BR', { minimumFractionDigits: 0 }) + ' K'; // Formatando em formato K para valores acima de 1000
                }
                return 'R$ ' + value.toLocaleString('pt-BR', {minimumFractionDigits: 2}); // Formatar o valor como moeda brasileira (R$)
            }
        },
        seriesIndex: false
    },
    colors: ['#229431'] // Mudando a cor das barras para laranja
};

var options_receber = {
    series: [{
        name: 'Total a Receber',
        data: valores_receber
    }],
    chart: {
        type: 'bar',
        height: 350,
        toolbar: {
            show: false
        },
        background: '#FFFFFF'
    },
    plotOptions: {
        bar: {
            horizontal: true,
            borderRadius: 3,
            columnWidth: '80%', // Largura das barras aumentada para 80%
            endingShape: 'rounded' // Mudança para pontas arredondadas
        }
    },
    dataLabels: {
        enabled: false,
        offsetX: -6,

    },
    title:{
        text: 'Contas a Receber',
        align: 'center',
        offsetY: 7,
        floating: true,
        style: {
          fontSize: '13px',
          color: '#082f4f'
        }
    },
    xaxis: {
        categories: categorias_receber,
        labels: {
            style: {
                fontSize: '12px',
                fontFamily: 'Helvetica, Arial, sans-serif'
            },
            formatter: function(val){
                return  Math.round(val / 1000).toLocaleString('pt-BR', { minimumFractionDigits: 0 }) + ' K';
            }
        }
    },
    grid: {
        show: false // Remover as linhas horizontais
    },
    tooltip: {
        enabled: true,
        shared: false,
        title: {
            text: 'Valor'
        },
        y: {
            
            formatter: function(value) {
                if (value >= 1000) {
                    return 'R$ ' + Math.round(value / 1000).toLocaleString('pt-BR', { minimumFractionDigits: 0 }) + ' K'; // Formatando em formato K para valores acima de 1000
                }
                return 'R$ ' + value.toLocaleString('pt-BR', {minimumFractionDigits: 2}); // Formatar o valor como moeda brasileira (R$)
            }
        },
        seriesIndex: false
    },
    colors: ['#229431'] // Mudando a cor das barras para laranja
};




var chart_pagar = new ApexCharts(document.querySelector("#chart-pagar"), options_pagar);
var chart_receber = new ApexCharts(document.querySelector("#chart-receber"), options_receber);
chart_pagar.render();
chart_receber.render();


