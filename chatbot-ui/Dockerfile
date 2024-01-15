FROM node:20.10.0-alpine AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

FROM base AS deps
WORKDIR /app

COPY .npmrc package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY chatbot-ui/package.json ./chatbot-ui/
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm --filter chatbot-ui install --frozen-lockfile

FROM base AS builder
WORKDIR /app

COPY .npmrc package.json pnpm-lock.yaml pnpm-workspace.yaml .prettierrc .prettierignore ./
COPY chatbot-ui ./chatbot-ui/
COPY --from=deps /app/node_modules ./node_modules
COPY --from=deps /app/chatbot-ui/node_modules ./chatbot-ui/node_modules
ARG NEXT_PUBLIC_BUILD_NUMBER
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm --filter chatbot-ui run build

FROM base AS runner
WORKDIR /app

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/chatbot-ui/public ./chatbot-ui/public

# Set the correct permission for prerender cache
#RUN mkdir .next
#RUN chown nextjs:nodejs .next

# Automatically leverage output traces to reduce image size
# https://nextjs.org/docs/advanced-features/output-file-tracing
COPY --from=builder --chown=nextjs:nodejs /app/chatbot-ui/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/chatbot-ui/.next/static ./chatbot-ui/.next/static

USER nextjs

ENV NODE_ENV=production
ENV PORT=3000
EXPOSE 3000

# server.js is created by next build from the standalone output
# https://nextjs.org/docs/pages/api-reference/next-config-js/output
CMD ["node", "chatbot-ui/server.js"]