using Documenter


include("pages.jl")

format = Documenter.HTML(prettyurls = get(ENV, "CI", nothing) == "true", 
                    ) 

makedocs(
    sitename = "Davai",
    format = format,
    pages = pages
)

deploydocs(
    repo = "github.com/ACCORD-NWP/DAVAI-env.git",
    devbranch = "main",   
    devurl = "main",
)
