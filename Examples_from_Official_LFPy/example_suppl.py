#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Some plottin' functions used by the example scripts

Copyright (C) 2017 Computational Neuroscience Group, NMBU.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import neuron
from matplotlib.collections import LineCollection

plt.rcParams.update({
    'axes.xmargin': 0.0,
    'axes.ymargin': 0.0,
})


def plot_ex1(cell, electrode, X, Y, Z):
    '''
    plot the morphology and LFP contours, synaptic current and soma trace
    '''
    # some plot parameters
    t_show = 30  # time point to show LFP
    tidx = np.where(cell.tvec == t_show)
    # contour lines:
    n_contours = 200
    n_contours_black = 40

    # This is the extracellular potential, reshaped to the X, Z mesh
    LFP = np.arcsinh(electrode.data[:, tidx]).reshape(X.shape)

    # figure object
    fig = plt.figure(figsize=(12, 8))
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None,
                        wspace=0.4, hspace=0.4)

    # Plot LFP around the cell with in color and with equipotential lines
    ax1 = fig.add_subplot(121, aspect='equal', frameon=False)

    # plot_morphology(plot_synapses=True)
    for sec in neuron.h.allsec():
        idx = cell.get_idx(sec.name())
        ax1.plot(np.r_[cell.x[idx, 0], cell.x[idx, 1][-1]],
                 np.r_[cell.z[idx, 0], cell.z[idx, 1][-1]],
                 color='k')
    for i in range(len(cell.synapses)):
        ax1.plot([cell.synapses[i].x], [cell.synapses[i].z], '.',
                 markersize=10)

    # contour lines
    ct1 = ax1.contourf(X, Z, LFP, n_contours)
    ct1.set_clim((-0.00007, 0.00002))
    ax1.contour(X, Z, LFP, n_contours_black, colors='k')

    # Plot synaptic input current
    ax2 = fig.add_subplot(222)
    ax2.plot(cell.tvec, cell.synapses[0].i)

    # Plot soma potential
    ax3 = fig.add_subplot(224)
    ax3.plot(cell.tvec, cell.somav)

    # Figure formatting and labels
    fig.suptitle('example 1', fontsize=14)

    ax1.set_title('LFP at t=' + str(t_show) + ' ms', fontsize=12)
    ax1.set_xticks([])
    ax1.set_xticklabels([])
    ax1.set_yticks([])
    ax1.set_yticklabels([])

    ax2.set_title('synaptic input current', fontsize=12)
    ax2.set_ylabel('(nA)')
    ax2.set_xlabel('time (ms)')

    ax3.set_title('somatic membrane potential', fontsize=12)
    ax3.set_ylabel('(mV)')
    ax3.set_xlabel('time (ms)')

    return fig


def plot_ex2(cell, electrode):
    '''example2.py plotting function'''
    # creating array of points and corresponding diameters along structure
    for i in range(cell.x.shape[0]):
        if i == 0:
            xcoords = np.array([cell.x[i].mean()])
            ycoords = np.array([cell.y[i].mean()])
            zcoords = np.array([cell.z[i].mean()])
            diams = np.array([cell.d[i]])
        else:
            if cell.z[i].mean() < 100 and cell.z[i].mean() > -100 and \
                    cell.x[i].mean() < 100 and cell.x[i].mean() > -100:
                xcoords = np.r_[xcoords,
                                np.linspace(cell.x[i, 0],
                                            cell.x[i, 1],
                                            int(cell.length[i] * 3))]
                ycoords = np.r_[ycoords,
                                np.linspace(cell.y[i, 0],
                                            cell.y[i, 1],
                                            int(cell.length[i] * 3))]
                zcoords = np.r_[zcoords,
                                np.linspace(cell.z[i, 0],
                                            cell.z[i, 1],
                                            int(cell.length[i] * 3))]
                diams = np.r_[diams,
                              np.linspace(cell.d[i], cell.d[i],
                                          int(cell.length[i] * 3))]

    # sort along depth-axis
    argsort = np.argsort(ycoords)

    # plotting
    fig = plt.figure(figsize=[12, 8])
    ax = fig.add_axes([0.1, 0.1, 0.533334, 0.8], frameon=False)
    ax.scatter(xcoords[argsort], zcoords[argsort], s=diams[argsort]**2 * 20,
               c=ycoords[argsort], edgecolors='none', cmap='gray')
    ax.plot(electrode.x, electrode.z, 'o', markersize=5, color='k')

    i = 0
    for LFP in electrode.data:
        tvec = cell.tvec * 0.6 + electrode.x[i] + 2
        if abs(LFP).max() >= 1:
            factor = 2
            color = 'r'
        elif abs(LFP).max() < 0.25:
            factor = 50
            color = 'b'
        else:
            factor = 10
            color = 'g'
        trace = LFP * factor + electrode.z[i]
        ax.plot(tvec, trace, color=color, lw=2)
        i += 1

    ax.plot([22, 28], [-60, -60], color='k', lw=3)
    ax.text(22, -65, '10 ms')

    ax.plot([40, 50], [-60, -60], color='k', lw=3)
    ax.text(42, -65, r'10 $\mu$m')

    ax.plot([60, 60], [20, 30], color='r', lw=2)
    ax.text(62, 20, '5 mV')

    ax.plot([60, 60], [0, 10], color='g', lw=2)
    ax.text(62, 0, '1 mV')

    ax.plot([60, 60], [-20, -10], color='b', lw=2)
    ax.text(62, -20, '0.1 mV')

    ax.set_xticks([])
    ax.set_yticks([])

    ax.axis([-61, 61, -61, 61])

    ax.set_title('Location-dependent extracellular spike shapes')

    # plotting the soma trace
    ax = fig.add_axes([0.75, 0.55, 0.2, 0.35])
    ax.plot(cell.tvec, cell.somav)
    ax.set_title('Somatic action-potential')
    ax.set_ylabel(r'$V_\mathrm{membrane}$ (mV)')

    # plotting the synaptic current
    ax = fig.add_axes([0.75, 0.1, 0.2, 0.35])
    ax.plot(cell.tvec, cell.synapses[0].i)
    ax.set_title('Synaptic current')
    ax.set_ylabel(r'$i_\mathrm{synapse}$ (nA)')
    ax.set_xlabel(r'time (ms)')

    return fig


def plot_ex3(cell, electrode):
    '''plotting function used by example3/4'''
    fig = plt.figure(figsize=[12, 8])

    # plot the somatic trace
    ax = fig.add_axes([0.1, 0.7, 0.5, 0.2])
    ax.plot(cell.tvec, cell.somav)
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Soma pot. (mV)')

    # plot the synaptic current
    ax = fig.add_axes([0.1, 0.4, 0.5, 0.2])
    for i in range(len(cell.synapses)):
        ax.plot(cell.tvec, cell.synapses[i].i,
                color='C0'
                if cell.synapses[i].kwargs['e'] > cell.v_init else 'C1',
                )
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel('Syn. i (nA)')

    # plot the LFP as image plot
    ax = fig.add_axes([0.1, 0.1, 0.5, 0.2])
    absmaxLFP = electrode.data.std() * 3
    im = ax.pcolormesh(cell.tvec, electrode.z, electrode.data,
                       vmax=absmaxLFP, vmin=-absmaxLFP,
                       cmap='PRGn',
                       shading='auto')

    rect = np.array(ax.get_position().bounds)
    rect[0] += rect[2] + 0.01
    rect[2] = 0.02
    cax = fig.add_axes(rect)
    cbar = plt.colorbar(im, cax=cax)
    cbar.set_label('LFP (mV)')
    ax.axis(ax.axis('tight'))
    ax.set_xlabel('Time (ms)')
    ax.set_ylabel(r'z ($\mu$m)')

    # plot the morphology, electrode contacts and synapses
    ax = fig.add_axes([0.65, 0.1, 0.25, 0.8], frameon=False)
    for sec in neuron.h.allsec():
        idx = cell.get_idx(sec.name())
        ax.plot(np.r_[cell.x[idx, 0], cell.x[idx, 1][-1]],
                np.r_[cell.z[idx, 0], cell.z[idx, 1][-1]],
                color='k')
    for i in range(len(cell.synapses)):
        ax.plot([cell.synapses[i].x], [cell.synapses[i].z], marker='.',
                color='C0'
                if cell.synapses[i].kwargs['e'] > cell.v_init else 'C1',
                )
    for i in range(electrode.x.size):
        ax.plot(electrode.x[i], electrode.z[i], color='C2', marker='o')
    ax.set_xticks([])
    ax.set_yticks([])

    return fig


def plotstuff(cell, electrode):
    '''plotting for spike waveform example'''
    fig = plt.figure(dpi=160)
    
    ax1 = fig.add_axes([0.05, 0.1, 0.55, 0.9], frameon=False)
    cax = fig.add_axes([0.05, 0.115, 0.55, 0.015])
    
    ax1.plot(electrode.x, electrode.z, 'o', markersize=1, color='k',
             zorder=0)
    
    #normalize to min peak
    LFPmin = electrode.data.min(axis=1)
    LFPnorm = -(electrode.data.T / LFPmin).T
    
    i = 0
    zips = []
    for x in LFPnorm:
        zips.append(list(zip(cell.tvec*1.6 + electrode.x[i] + 2,
                        x*12 + electrode.z[i])))
        i += 1
    
    line_segments = LineCollection(zips,
                                    linewidths = (1),
                                    linestyles = 'solid',
                                    cmap='nipy_spectral',
                                    zorder=1,
                                    rasterized=False)
    line_segments.set_array(np.log10(-LFPmin))
    ax1.add_collection(line_segments)
    
    axcb = fig.colorbar(line_segments, cax=cax, orientation='horizontal')
    axcb.outline.set_visible(False)
    xticklabels = np.array([-0.1  , -0.05 , -0.02 , -0.01 , -0.005, -0.002])
    xticks = np.log10(-xticklabels)
    axcb.set_ticks(xticks)
    axcb.set_ticklabels(np.round(-10**xticks, decimals=3))  
    axcb.set_label('spike amplitude (mV)', va='center')
    
    ax1.plot([22, 38], [100, 100], color='k', lw = 1)
    ax1.text(22, 102, '10 ms')
    
    ax1.plot([60, 80], [100, 100], color='k', lw = 1)
    ax1.text(60, 102, '20 $\mu$m')
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    axis = ax1.axis(ax1.axis('equal'))
    ax1.set_xlim(axis[0]*1.02, axis[1]*1.02)
    
    # plot morphology
    zips = []
    for x, z in cell.get_pt3d_polygons():
        zips.append(list(zip(x, z)))
    from matplotlib.collections import PolyCollection
    polycol = PolyCollection(zips, edgecolors='none',
                             facecolors='gray', zorder=-1, rasterized=False)
    ax1.add_collection(polycol)

    ax1.text(-0.05, 0.95, 'a',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=16, fontweight='demibold',
        transform=ax1.transAxes)
    

    # plot extracellular spike in detail
    ind = np.where(electrode.data == electrode.data.min())[0][0]
    timeind = (cell.tvec >= 0) & (cell.tvec <= 10)
    xticks = np.arange(10)
    xticklabels = xticks
    LFPtrace = electrode.data[ind, ]
    vline0 = cell.tvec[cell.somav==cell.somav.max()]
    vline1 = cell.tvec[LFPtrace == LFPtrace.min()]
    vline2 = cell.tvec[LFPtrace == LFPtrace.max()]
    
    # plot asterix to link trace in (a) and (c)
    ax1.plot(electrode.x[ind], electrode.z[ind], '*', markersize=5, 
             markeredgecolor='none', markerfacecolor='k')
    
    ax2 = fig.add_axes([0.75, 0.6, 0.2, 0.35], frameon=True)
    ax2.plot(cell.tvec[timeind], cell.somav[timeind], lw=1, color='k', clip_on=False)
    
    ax2.vlines(vline0, cell.somav.min(), cell.somav.max(), 'k', 'dashed', lw=0.25)
    ax2.vlines(vline1, cell.somav.min(), cell.somav.max(), 'k', 'dashdot', lw=0.25)
    ax2.vlines(vline2, cell.somav.min(), cell.somav.max(), 'k', 'dotted', lw=0.25)
    
    ax2.set_xticks(xticks)
    ax2.set_xticklabels(xticks)
    ax2.axis(ax2.axis('tight'))
    ax2.set_ylabel(r'$V_\mathrm{soma}(t)$ (mV)')
    
    for loc, spine in ax2.spines.items():
        if loc in ['right', 'top']:
            spine.set_color('none')            
    ax2.xaxis.set_ticks_position('bottom')
    ax2.yaxis.set_ticks_position('left')
    
    ax2.set_title('somatic potential', va='center')

    ax2.text(-0.3, 1.0, 'b',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=16, fontweight='demibold',
        transform=ax2.transAxes)

    ax3 = fig.add_axes([0.75, 0.1, 0.2, 0.35], frameon=True)
    ax3.plot(cell.tvec[timeind], LFPtrace[timeind], lw=1, color='k', clip_on=False)
    ax3.plot(0.5, 0, '*', markersize=5, markeredgecolor='none', markerfacecolor='k')

    ax3.vlines(vline0, LFPtrace.min(), LFPtrace.max(), 'k', 'dashed', lw=0.25)
    ax3.vlines(vline1, LFPtrace.min(), LFPtrace.max(), 'k', 'dashdot', lw=0.25)
    ax3.vlines(vline2, LFPtrace.min(), LFPtrace.max(), 'k', 'dotted', lw=0.25)

    ax3.set_xticks(xticks)
    ax3.set_xticklabels(xticks)
    ax3.axis(ax3.axis('tight'))
    
    for loc, spine in ax3.spines.items():
        if loc in ['right', 'top']:
            spine.set_color('none')            
    ax3.xaxis.set_ticks_position('bottom')
    ax3.yaxis.set_ticks_position('left')

    ax3.set_xlabel(r'$t$ (ms)', va='center')
    ax3.set_ylabel(r'$\Phi(\mathbf{r},t)$ (mV)')
                   
    ax3.set_title('extracellular spike', va='center')

    ax3.text(-0.3, 1.0, 'c',
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=16, fontweight='demibold',
        transform=ax3.transAxes)

    return fig