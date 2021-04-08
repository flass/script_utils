#!/usr/bin/env Rscript
trues = c('+', '1', 't', 'T', 'true', 'yes', 'TRUE')

write.iTol.dataset.table.bin = function(df, cols, colcolours, dataset_label, nfout=NULL, outdir=NULL, field_shapes=1, height_factor=1){
    if (is.null(nfout)) nfout = file.path(outdir, paste(gsub(" ", "_", dataset_label), 'iTol.dataset_binary.txt', sep='.'))
    write("DATASET_BINARY", file=nfout)
    write("SEPARATOR TAB", file=nfout, append=T)
    write(sprintf("DATASET_LABEL	%s", dataset_label), file=nfout, append=T)
    write(paste("LEGEND_TITLE", dataset_label, sep='\t'), file=nfout, append=T)
	colshapes = c(rep(field_shapes, length(cols)%/%length(field_shapes)), field_shapes[length(cols)%%length(field_shapes)])
    write(paste("LEGEND_LABELS", paste(cols, collapse='\t'), sep='\t'), file=nfout, append=T)
    write(paste("LEGEND_SHAPES", paste(colshapes, collapse='\t'), sep='\t'), file=nfout, append=T)
    write(paste("LEGEND_COLORS", paste(colcolours[1:length(cols)], collapse='\t'), sep='\t'), file=nfout, append=T)
    write(paste("FIELD_LABELS", paste(cols, collapse='\t'), sep='\t'), file=nfout, append=T)
    write(paste("FIELD_SHAPES", paste(colshapes, collapse='\t'), sep='\t'), file=nfout, append=T)
    write(paste("FIELD_COLORS", paste(colcolours[1:length(cols)], collapse='\t'), sep='\t'), file=nfout, append=T)
    t = df[,c('Isolate.name', cols)]
    for (col in cols){
        if (!is.logical(t[,col])){
            t[,col] = ifelse(as.character(t[,col]) %in% trues, 1, -1)
        }else{
            t[,col] = ifelse(t[,col], 1, -1)
        }
    }
    write(paste("HEIGHT_FACTOR", height_factor, sep='\t'), file=nfout, append=T)
    write("DATA", file=nfout, append=T)
    write.table(t, file=nfout, sep='\t', col.names=F, row.names=F, quote=F, append=T)

}

write.iTol.dataset.table.bin.colstrip = function(df, col, colcolours, collabels, nfout=NULL, outdir=NULL){
    if (is.null(nfout)) nfout = file.path(outdir, paste(col, 'iTol.dataset_bin_colourstrip.txt', sep='.'))
    write("DATASET_COLORSTRIP", file=nfout)
    write("SEPARATOR TAB", file=nfout, append=T)
    write(sprintf("DATASET_LABEL	%s", col), file=nfout, append=T)
    write("COLOR_BRANCHES	0", file=nfout, append=T)
    t = df[,c('Isolate.name', col)]
    t[['Color']] = ifelse(t[[col]], colcolours[1], colcolours[2])
    t[['Label']] = ifelse(t[[col]], collabels[1], collabels[2])
    write("DATA", file=nfout, append=T)
    write.table(t[,c('Isolate.name', 'Color', 'Label')], file=nfout, sep='\t', col.names=F, row.names=F, quote=F, append=T)

}

write.iTol.dataset.table.fac.colstrip = function(df, col, colcolours, nfout=NULL, outdir=NULL, colour_branches=FALSE){
	if (nrow(df)<1){
		print("Warning: input df has 0 rows; do not write ouput file")
	}else{
		if (is.null(nfout)) nfout = file.path(outdir, paste(col, 'iTol.dataset_multi_colourstrip.txt', sep='.'))
		write("DATASET_COLORSTRIP", file=nfout)
		write("SEPARATOR TAB", file=nfout, append=T)
		write(sprintf("DATASET_LABEL	%s", col), file=nfout, append=T)
		if (colour_branches){ write("COLOR_BRANCHES	1", file=nfout, append=T)
		}else{ write("COLOR_BRANCHES	0", file=nfout, append=T) }
		t = df[,c('Isolate.name', col)]
		fac = as.factor(t[[col]])
		f = levels(fac)
		k = as.numeric(fac)
		write(paste("LEGEND_TITLE", col, sep='\t'), file=nfout, append=T)
		write(paste("LEGEND_LABELS", paste(f, collapse='\t'), sep='\t'), file=nfout, append=T)
		write(paste("LEGEND_COLORS", paste(colcolours[1:length(f)], collapse='\t'), sep='\t'), file=nfout, append=T)
		write(paste("LEGEND_SHAPES", paste(rep(1, length(f)), collapse='\t'), sep='\t'), file=nfout, append=T)
		write(paste("BORDER_WIDTH", 0.5, sep='\t'), file=nfout, append=T)
		write(paste("BORDER_COLOR", "#000000", sep='\t'), file=nfout, append=T)
		t[['Color']] = ifelse(is.na(k), "#FFFFFFFF", colcolours[k])
		t[['Label']] = t[[col]]
		write("DATA", file=nfout, append=T)
		write.table(t[,c('Isolate.name', 'Color', 'Label')], file=nfout, sep='\t', col.names=F, row.names=F, quote=F, append=T)
	}
}

write.iTol.dataset.table.fac.clade.treecols = function(df, col, colcolours, nfout=NULL, outdir=NULL){
	if (is.null(nfout)) nfout = file.path(outdir, paste(col, 'iTol.dataset_caldetreecols.txt', sep='.'))
	write("TREE_COLORS", file=nfout)
    write("SEPARATOR TAB", file=nfout, append=T)
    t = df[,c('clade_id', col)]
    fac = as.factor(t[[col]])
    f = levels(fac)
    k = as.numeric(fac)
    t[['Color']] = ifelse(is.na(k), "#FFFFFFFF", colcolours[k])
    t[['Label']] = t[[col]]
	t[['Type']] = 'range'
    write("DATA", file=nfout, append=T)
    write.table(t[,c('clade_id', 'Type', 'Color', 'Label')], file=nfout, sep='\t', col.names=F, row.names=F, quote=F, append=T)
}