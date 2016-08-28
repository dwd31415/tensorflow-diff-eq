using Plots
using NPZ
using ProgressMeter

# load the simulated data
data = npzread("../lorenz_sim_data.npy")
n = 2000

# initialize 3d plot
plt = path3d(1, xlim=(-25,25), ylim=(-25,25), zlim=(0,50),
                xlab = "x", ylab = "y", zlab = "z",
                markercolor=RGBA(254/255,190/255,31/255,250/255),
                title = "Lorenz Attractor", marker = 1)

# plot simulated data
p = Progress(n, 0.01)
anim = @animate for i=1:n
    push!(plt, data[1,i], data[2,i], data[3,i])
    update!(p, i)
end every 3

gif(anim, "./simulated_lorenz_attractor.gif", fps = 15)
