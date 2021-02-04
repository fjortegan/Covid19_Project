## ----global_options, include=FALSE---------------------------------------------------
#Sys.setlocale('LC_ALL','C') # corrige problema con (ocasionaba problemas con acentos en fig.cap)
options(kableExtra.latex.load_packages = F)
#options(tinytex.latexmk.emulation = FALSE)
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = TRUE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE) # 
knitr::write_bib(c("knitr","rmarkdown","dplyr","ggplot2","kableExtra"),
                 file="bib/paquetes.bib", width = 60)


## ----child = 'prologo.Rmd'-----------------------------------------------------------




## ----child = 'resumen.Rmd'-----------------------------------------------------------




## ----child = 'abstract.Rmd'----------------------------------------------------------




## ----child = 'capitulo01.Rmd'--------------------------------------------------------

## ----include=FALSE-------------------------------------------------------------------
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = FALSE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE)




## ----child = 'capitulo02.Rmd'--------------------------------------------------------

## ----include=FALSE-------------------------------------------------------------------
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = FALSE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE)




## ----child = 'capitulo03.Rmd'--------------------------------------------------------

## ----include=FALSE-------------------------------------------------------------------
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = FALSE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE)




## ----child = 'capitulo04.Rmd'--------------------------------------------------------

## ----include=FALSE-------------------------------------------------------------------
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = FALSE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE)




## ----child = 'apendice01.Rmd'--------------------------------------------------------

## ----include=FALSE-------------------------------------------------------------------
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = FALSE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE)




## ----child = 'apendice02.Rmd'--------------------------------------------------------

## ----include=FALSE-------------------------------------------------------------------
knitr::opts_chunk$set(fig.path = 'figurasR/',
                      echo = FALSE, warning = FALSE, message = FALSE,
                      fig.pos="H",fig.align="center",out.width="95%",
                      cache=FALSE)



